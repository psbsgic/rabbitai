# -*- coding: utf-8 -*-

import copy
import math
from typing import Any, Callable, cast, Dict, List, Optional, TYPE_CHECKING

from flask_babel import _

from rabbitai import app
from rabbitai.connectors.base.models import BaseDatasource
from rabbitai.exceptions import QueryObjectValidationError
from rabbitai.utils.core import (
    ChartDataResultType,
    extract_column_dtype,
    extract_dataframe_dtypes,
    get_time_filter_status,
    QueryStatus,
)

if TYPE_CHECKING:
    from rabbitai.common.query_context import QueryContext
    from rabbitai.common.query_object import QueryObject

config = app.config


def _get_datasource(query_context: "QueryContext", query_obj: "QueryObject") -> BaseDatasource:
    """
    获取数据源对象。

    :param query_context:
    :param query_obj:
    :return:
    """
    return query_obj.datasource or query_context.datasource


def _get_columns(
    query_context: "QueryContext", query_obj: "QueryObject", _: bool
) -> Dict[str, Any]:
    """
    获取列元数据，{column_name：<列名称>、verbose_name：<显示名称>、dtype：<数据类型>} 的列表。

    :param query_context: 查询上下文。
    :param query_obj: 查询对象。
    :param _:
    :return:
    """

    datasource = _get_datasource(query_context, query_obj)

    return {
        "data": [
            {
                "column_name": col.column_name,
                "verbose_name": col.verbose_name,
                "dtype": extract_column_dtype(col),
            }
            for col in datasource.columns
        ]
    }


def _get_timegrains(
    query_context: "QueryContext", query_obj: "QueryObject", _: bool
) -> Dict[str, Any]:
    """
    获取时间粒度数据。

    :param query_context:
    :param query_obj:
    :param _:
    :return:
    """
    datasource = _get_datasource(query_context, query_obj)
    return {
        "data": [
            {
                "name": grain.name,
                "function": grain.function,
                "duration": grain.duration,
            }
            for grain in datasource.database.grains()
        ]
    }


def _get_query(
    query_context: "QueryContext", query_obj: "QueryObject", _: bool,
) -> Dict[str, Any]:
    """
    获取查询。

    :param query_context:
    :param query_obj:
    :param _:
    :return:
    """
    datasource = _get_datasource(query_context, query_obj)
    result = {"language": datasource.query_language}
    try:
        result["query"] = datasource.get_query_str(query_obj.to_dict())
    except QueryObjectValidationError as err:
        result["error"] = err.message
    return result


def _get_full(
    query_context: "QueryContext",
    query_obj: "QueryObject",
    force_cached: Optional[bool] = False,
) -> Dict[str, Any]:
    datasource = _get_datasource(query_context, query_obj)
    result_type = query_obj.result_type or query_context.result_type
    payload = query_context.get_df_payload(query_obj, force_cached=force_cached)
    df = payload["df"]
    status = payload["status"]
    if status != QueryStatus.FAILED:
        payload["colnames"] = list(df.columns)
        payload["coltypes"] = extract_dataframe_dtypes(df)
        payload["data"] = query_context.get_data(df)
    del payload["df"]

    filters = query_obj.filter
    filter_columns = cast(List[str], [flt.get("col") for flt in filters])
    columns = set(datasource.column_names)
    applied_time_columns, rejected_time_columns = get_time_filter_status(
        datasource, query_obj.applied_time_extras
    )
    payload["applied_filters"] = [
        {"column": col} for col in filter_columns if col in columns
    ] + applied_time_columns
    payload["rejected_filters"] = [
        {"reason": "not_in_datasource", "column": col}
        for col in filter_columns
        if col not in columns
    ] + rejected_time_columns

    if result_type == ChartDataResultType.RESULTS and status != QueryStatus.FAILED:
        return {"data": payload.get("data")}
    return payload


def _get_samples(
    query_context: "QueryContext", query_obj: "QueryObject", force_cached: bool = False
) -> Dict[str, Any]:
    datasource = _get_datasource(query_context, query_obj)
    row_limit = query_obj.row_limit or math.inf
    query_obj = copy.copy(query_obj)
    query_obj.is_timeseries = False
    query_obj.orderby = []
    query_obj.groupby = []
    query_obj.metrics = []
    query_obj.post_processing = []
    query_obj.row_limit = min(row_limit, config["SAMPLES_ROW_LIMIT"])
    query_obj.row_offset = 0
    query_obj.columns = [o.column_name for o in datasource.columns]
    return _get_full(query_context, query_obj, force_cached)


def _get_results(
    query_context: "QueryContext", query_obj: "QueryObject", force_cached: bool = False
) -> Dict[str, Any]:
    payload = _get_full(query_context, query_obj, force_cached)
    return {"data": payload.get("data"), "error": payload.get("error")}


_result_type_functions: Dict[
    ChartDataResultType, Callable[["QueryContext", "QueryObject", bool], Dict[str, Any]]
] = {
    ChartDataResultType.COLUMNS: _get_columns,
    ChartDataResultType.TIMEGRAINS: _get_timegrains,
    ChartDataResultType.QUERY: _get_query,
    ChartDataResultType.SAMPLES: _get_samples,
    ChartDataResultType.FULL: _get_full,
    ChartDataResultType.RESULTS: _get_results,
    # for requests for post-processed data we return the full results,
    # and post-process it later where we have the chart context, since
    # post-processing is unique to each visualization type
    ChartDataResultType.POST_PROCESSED: _get_full,
}
"""图表数据结果类型（COLUMNS、TIMEGRAINS、QUERY、SAMPLES、FULL、RESULTS、POST_PROCESSED）及其结果获取函数的字典。"""


def get_query_results(
    result_type: ChartDataResultType,
    query_context: "QueryContext",
    query_obj: "QueryObject",
    force_cached: bool,
) -> Dict[str, Any]:
    """
    基于图表数据请求，返回查询结果。

    :param result_type: 要返回结果的类型。
    :param query_context: 查询上下文对象。
    :param query_obj: 用于提取查询结果的查询对象。
    :param force_cached: 是否强制从缓存获取查询结果。
    :raises QueryObjectValidationError: 如果不支持的结果类型。
    :return: JSON 结果。
    """

    result_func = _result_type_functions.get(result_type)
    if result_func:
        return result_func(query_context, query_obj, force_cached)

    raise QueryObjectValidationError(
        _("Invalid result type: %(result_type)s", result_type=result_type)
    )
