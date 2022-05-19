# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, Optional

from flask_caching import Cache
from pandas import DataFrame

from rabbitai import app
from rabbitai.constants import CacheRegion
from rabbitai.exceptions import CacheLoadError
from rabbitai.extensions import cache_manager
from rabbitai.models.helpers import QueryResult
from rabbitai.stats_logger import BaseStatsLogger
from rabbitai.utils.cache import set_and_log_cache
from rabbitai.utils.core import error_msg_from_exception, get_stacktrace, QueryStatus

config = app.config
stats_logger: BaseStatsLogger = config["STATS_LOGGER"]
logger = logging.getLogger(__name__)

_cache: Dict[CacheRegion, Cache] = {
    CacheRegion.DEFAULT: cache_manager.cache,
    CacheRegion.DATA: cache_manager.data_cache,
}


class QueryCacheManager:
    """
    查询缓存管理器。

    包括以下参数：

    - df: DataFrame = DataFrame(),
    - query: str = "",
    - annotation_data: Optional[Dict[str, Any]] = None,
    - status: Optional[str] = None,
    - error_message: Optional[str] = None,
    - is_loaded: bool = False,
    - stacktrace: Optional[str] = None,
    - is_cached: Optional[bool] = None,
    - cache_dttm: Optional[str] = None,
    - cache_value: Optional[Dict[str, Any]] = None,

    """

    def __init__(
        self,
        df: DataFrame = DataFrame(),
        query: str = "",
        annotation_data: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
        error_message: Optional[str] = None,
        is_loaded: bool = False,
        stacktrace: Optional[str] = None,
        is_cached: Optional[bool] = None,
        cache_dttm: Optional[str] = None,
        cache_value: Optional[Dict[str, Any]] = None,
    ) -> None:
        """

        :param df: 数据帧。
        :param query: 查询字符串。
        :param annotation_data: 注释数据字典。
        :param status: 状态。
        :param error_message: 错误信息。
        :param is_loaded: 是否已加载。
        :param stacktrace: 堆栈跟踪。
        :param is_cached: 是否已缓存。
        :param cache_dttm: 缓存时间。
        :param cache_value: 缓存值。
        """
        self.df = df
        self.query = query
        self.annotation_data = {} if annotation_data is None else annotation_data
        self.status = status
        self.error_message = error_message

        self.is_loaded = is_loaded
        self.stacktrace = stacktrace
        self.is_cached = is_cached
        self.cache_dttm = cache_dttm
        self.cache_value = cache_value

    def set_query_result(
        self,
        key: str,
        query_result: QueryResult,
        annotation_data: Optional[Dict[str, Any]] = None,
        force_query: Optional[bool] = False,
        timeout: Optional[int] = None,
        datasource_uid: Optional[str] = None,
        region: CacheRegion = CacheRegion.DEFAULT,
    ) -> None:
        """
        设置指定查询结果的数据帧到指定缓存区。

        :param key: 键。
        :param query_result: 查询结果。
        :param annotation_data: 注释数据。
        :param force_query: 是否强制查询。
        :param timeout: 超时。
        :param datasource_uid: 数据源对象标识。
        :param region: 缓存区。
        :return:
        """

        try:
            self.status = query_result.status
            self.query = query_result.query
            self.error_message = query_result.error_message
            self.df = query_result.df
            self.annotation_data = {} if annotation_data is None else annotation_data

            if self.status != QueryStatus.FAILED:
                stats_logger.incr("loaded_from_source")
                if not force_query:
                    stats_logger.incr("loaded_from_source_without_force")
                self.is_loaded = True

            value = {
                "df": self.df,
                "query": self.query,
                "annotation_data": self.annotation_data,
            }
            if self.is_loaded and key and self.status != QueryStatus.FAILED:
                self.set(
                    key=key,
                    value=value,
                    timeout=timeout,
                    datasource_uid=datasource_uid,
                    region=region,
                )
        except Exception as ex:  # pylint: disable=broad-except
            logger.exception(ex)
            if not self.error_message:
                self.error_message = str(ex)
            self.status = QueryStatus.FAILED
            self.stacktrace = get_stacktrace()

    @classmethod
    def get(
        cls,
        key: Optional[str],
        region: CacheRegion = CacheRegion.DEFAULT,
        force_query: Optional[bool] = False,
        force_cached: Optional[bool] = False,
    ) -> "QueryCacheManager":
        """
        依据指定查询缓存键，获取查询缓存管理器 QueryCacheManager。

        :param key: 键。
        :param region: 缓存区。
        :param force_query: 是否强制查询。
        :param force_cached: 是否强制缓存。
        :return:
        """

        query_cache = cls()
        if not key or not _cache[region] or force_query:
            return query_cache

        cache_value = _cache[region].get(key)
        if cache_value:
            logger.info("Cache key: %s", key)
            stats_logger.incr("loading_from_cache")
            try:
                query_cache.df = cache_value["df"]
                query_cache.query = cache_value["query"]
                query_cache.annotation_data = cache_value.get("annotation_data", {})
                query_cache.status = QueryStatus.SUCCESS
                query_cache.is_loaded = True
                query_cache.is_cached = cache_value is not None
                query_cache.cache_dttm = (
                    cache_value["dttm"] if cache_value is not None else None
                )
                query_cache.cache_value = cache_value
                stats_logger.incr("loaded_from_cache")
            except KeyError as ex:
                logger.exception(ex)
                logger.error(
                    "Error reading cache: %s",
                    error_msg_from_exception(ex),
                    exc_info=True,
                )
            logger.info("Serving from cache")

        if force_cached and not query_cache.is_loaded:
            logger.warning(
                "force_cached (QueryContext): value not found for key %s", key
            )
            raise CacheLoadError("Error loading data from cache")
        return query_cache

    @staticmethod
    def set(
        key: Optional[str],
        value: Dict[str, Any],
        timeout: Optional[int] = None,
        datasource_uid: Optional[str] = None,
        region: CacheRegion = CacheRegion.DEFAULT,
    ) -> None:
        """
        set value to specify cache region, proxy for `set_and_log_cache`

        :param key:
        :param value:
        :param timeout:
        :param datasource_uid:
        :param region:
        :return:
        """

        if key:
            set_and_log_cache(_cache[region], key, value, timeout, datasource_uid)
