# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flask import Flask
from flask_caching import Cache
from typing_extensions import TypedDict
from werkzeug.wrappers import Response


class AdhocMetricColumn(TypedDict):
    """动态（Adhoc）指标列类型，定义column_name、type及其数据类型。"""

    column_name: Optional[str]
    """列名称"""
    type: str
    """列数据类型名称"""


class AdhocMetric(TypedDict):
    """动态（Adhoc）指标类型，定义：aggregate、column、expressionType、label、sqlExpression及其数据类型。"""

    aggregate: str
    """聚合函数名称"""
    column: AdhocMetricColumn
    """动态指标列"""
    expressionType: str
    """表达式类型"""
    label: str
    """标签文本，作为显示名称"""
    sqlExpression: Optional[str]
    """SQL表达式字符串"""


CacheConfig = Union[Callable[[Flask], Cache], Dict[str, Any]]
"""缓存配置类型，可调用对象或字典"""
DbapiDescriptionRow = Tuple[
    str, str, Optional[str], Optional[str], Optional[int], Optional[int], bool
]
"""数据库API行描述类型，str, str, Optional[str], Optional[str], Optional[int], Optional[int], bool的元组。"""
DbapiDescription = Union[List[DbapiDescriptionRow], Tuple[DbapiDescriptionRow, ...]]
"""数据库API描述，DbapiDescriptionRow的列表或元组"""
DbapiResult = Sequence[Union[List[Any], Tuple[Any, ...]]]
"""数据库结果类型，列表或元组序列"""
FilterValue = Union[bool, datetime, float, int, str]
"""过滤值类型，bool, datetime, float, int, str之一"""
FilterValues = Union[FilterValue, List[FilterValue], Tuple[FilterValue]]
"""过滤值集合类型，FilterValue, List[FilterValue], Tuple[FilterValue]之一"""
FormData = Dict[str, Any]
"""表单数据类型，字符串键和任意值的字典集合"""
Granularity = Union[str, Dict[str, Union[str, float]]]
"""时间粒度类型，字符串或字典集合"""
Metric = Union[AdhocMetric, str]
"""指标类型，动态指标类型AdhocMetric或指标名称str"""
OrderBy = Tuple[Metric, bool]
"""排序类型，Metric和bool的元组"""
QueryObjectDict = Dict[str, Any]
"""查询对象字典类型，字符串键和任意值的字典集合"""
VizData = Optional[Union[List[Any], Dict[Any, Any]]]
"""可视数据类型，List[Any]或Dict[Any, Any]"""
VizPayload = Dict[str, Any]
"""可视载荷类型，字符串键和任意值的字典集合"""

# Flask response.
Base = Union[bytes, str]
"""基本类型，bytes或str"""
Status = Union[int, str]
"""状态类型，int或str"""
Headers = Dict[str, Any]
"""标头集合类型，字符串键和任意值的字典集合"""
FlaskResponse = Union[
    Response,
    Base,
    Tuple[Base, Status],
    Tuple[Base, Status, Headers],
    Tuple[Response, Status],
]
"""Flask响应对象类型，Response、Base、Tuple[Base, Status]、Tuple[Base, Status, Headers]、Tuple[Response, Status]之一"""
