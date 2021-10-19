# -*- coding: utf-8 -*-

from flask import Flask
from flask_caching import Cache


class CacheManager:
    """
    缓存管理器，依据应用配置提供的信息构建缓存实例，并提供访问。

    创建 Cache 类型的应用缓存、数据缓存和缩略图缓存。
    """

    def __init__(self) -> None:
        """初始化新实例，创建 Cache 类型的应用缓存、数据缓存和缩略图缓存。"""

        super().__init__()

        self._cache = Cache()
        self._data_cache = Cache()
        self._thumbnail_cache = Cache()

    def init_app(self, app: Flask) -> None:
        """
        依据指定应用实例的配置对象提供的缓存相关选项，分别初始化应用缓存、数据缓存和缩略图缓存。

        :param app:
        :return:
        """

        self._cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["CACHE_CONFIG"],
            },
        )
        self._data_cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["DATA_CACHE_CONFIG"],
            },
        )
        self._thumbnail_cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["THUMBNAIL_CACHE_CONFIG"],
            },
        )

    @property
    def data_cache(self) -> Cache:
        return self._data_cache

    @property
    def cache(self) -> Cache:
        return self._cache

    @property
    def thumbnail_cache(self) -> Cache:
        return self._thumbnail_cache
