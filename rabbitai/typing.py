from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flask import Flask
from flask_caching import Cache
from werkzeug.wrappers import Response

CacheConfig = Union[Callable[[Flask], Cache], Dict[str, Any]]
"""缓存配置，可调用对象或字典"""
DbapiDescriptionRow = Tuple[str, str, Optional[str], Optional[str], Optional[int], Optional[int], bool]
"""DB接口描述行数据类型。"""
DbapiDescription = Union[List[DbapiDescriptionRow], Tuple[DbapiDescriptionRow, ...]]
"""DB接口描述"""
DbapiResult = Sequence[Union[List[Any], Tuple[Any, ...]]]
"""DB接口结果，序列"""
FilterValue = Union[datetime, float, int, str]
"""过滤值，日期时间、浮点、整数、字符串"""
FilterValues = Union[FilterValue, List[FilterValue], Tuple[FilterValue]]
"""过滤值集，FilterValue、FilterValue的列表、FilterValue的元组"""
FormData = Dict[str, Any]
"""表单数据类型，字典"""
Granularity = Union[str, Dict[str, Union[str, float]]]
"""粒度，字符串或字典"""
AdhocMetric = Dict[str, Any]
"""特定指标，字典"""
Metric = Union[AdhocMetric, str]
"""指标，AdhocMetric或字符串"""
OrderBy = Tuple[Metric, bool]
"""排序，（Metric, bool）"""
QueryObjectDict = Dict[str, Any]
"""查询对象字典。"""
VizData = Optional[Union[List[Any], Dict[Any, Any]]]
"""可视数据，列表或字典"""
VizPayload = Dict[str, Any]
"""可视载荷，字典"""

# Flask response.
Base = Union[bytes, str]
"""响应基础数据，字节或字符串"""
Status = Union[int, str]
"""状态，整数或字符串"""
Headers = Dict[str, Any]
"""响应标头，字典"""
FlaskResponse = Union[Response, Base, Tuple[Base, Status], Tuple[Base, Status, Headers],]
"""响应对象，Response、Base、（Base, Status）、（Base, Status, Headers）"""
