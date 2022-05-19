# pylint: disable=R
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple, Optional

from flask_babel import gettext as _
from pandas import DataFrame

from rabbitai import app, db
from rabbitai.connectors.base.models import BaseDatasource
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.exceptions import QueryObjectValidationError
from rabbitai.typing import Metric, OrderBy
from rabbitai.utils import pandas_postprocessing
from rabbitai.utils.core import (
    ChartDataResultType,
    DatasourceDict,
    DTTM_ALIAS,
    find_duplicates,
    get_metric_names,
    is_adhoc_metric,
    json_int_dttm_ser,
    QueryObjectFilterClause,
)
from rabbitai.utils.date_parser import get_since_until, parse_human_timedelta
from rabbitai.utils.hashing import md5_sha_from_dict
from rabbitai.views.utils import get_time_range_endpoints

config = app.config
logger = logging.getLogger(__name__)


class DeprecatedField(NamedTuple):
    old_name: str
    new_name: str


DEPRECATED_FIELDS = (
    DeprecatedField(old_name="granularity_sqla", new_name="granularity"),
)

DEPRECATED_EXTRAS_FIELDS = (
    DeprecatedField(old_name="where", new_name="where"),
    DeprecatedField(old_name="having", new_name="having"),
    DeprecatedField(old_name="having_filters", new_name="having_druid"),
    DeprecatedField(old_name="druid_time_origin", new_name="druid_time_origin"),
)


class QueryObject:
    """
    查询对象，查询对象的结构与数据库连接器（如sqla和druid）的接口相匹配。查询对象是在客户机上构造的。

    包括以下参数：

    - datasource: 数据源对象，可选。
    - result_type: 返回结果类型 ChartDataResultType，可选。
    - annotation_layers: 注释层（字典的列表），可选。
    - applied_time_extras: 应用的自定义时间（字典的列表），可选。
    - apply_fetch_values_predicate: 是否应用提取值判断。
    - granularity: 时间粒度。
    - metrics: 指标列表。
    - groupby: 分组列名称的列表。
    - filters: 过滤器 QueryObjectFilterClause 的列表。
    - time_range: 时间范围。
    - time_shift: 时间位移。
    - is_timeseries: 是否时间序列。
    - timeseries_limit: 时间序列限制。
    - row_limit: 行限制。
    - row_offset: 行位移。
    - timeseries_limit_metric: 时间序列限制指标。
    - order_desc: 是否降序。
    - extras: 自定义数据。
    - columns: 列集合。
    - orderby: 排序列
    - post_processing: 后处理。
    - is_rowcount: 是否行计数。

    """

    # region 类属性

    annotation_layers: List[Dict[str, Any]]
    """注释层的列表"""
    applied_time_extras: Dict[str, str]
    """应用的时间额外数据字典"""
    apply_fetch_values_predicate: bool
    """是否应用提取值预测"""
    granularity: Optional[str]
    """粒度"""
    from_dttm: Optional[datetime]
    """开始时间"""
    to_dttm: Optional[datetime]
    """结束时间"""
    inner_from_dttm: Optional[datetime]
    """内部开始时间"""
    inner_to_dttm: Optional[datetime]
    """内部结束时间"""
    is_timeseries: bool
    """是否时间序列"""
    time_shift: Optional[timedelta]
    """时间偏移"""
    groupby: List[str]
    """分组字段列表"""
    metrics: Optional[List[Metric]]
    """指标列表"""
    row_limit: int
    """行限制"""
    row_offset: int
    """行位移"""
    filter: List[QueryObjectFilterClause]
    """查询对象过滤器的列表"""
    timeseries_limit: int
    """时间序列限制"""
    timeseries_limit_metric: Optional[Metric]
    """时间序列限制指标"""
    order_desc: bool
    """是否排序"""
    extras: Dict[str, Any]
    """额外数据（字典）"""
    columns: List[str]
    """列名称的列表"""
    orderby: List[OrderBy]
    """排序表达式的列表"""
    post_processing: List[Dict[str, Any]]
    """对数据帧要进行的后处理操作，操作和选项字典的列表。"""
    datasource: Optional[BaseDatasource]
    """数据源对象"""
    result_type: Optional[ChartDataResultType]
    """结果类型"""
    is_rowcount: bool
    """是否行数"""
    time_offsets: List[str]
    """时间位移列表"""

    # endregion

    def __init__(
        self,
        datasource: Optional[DatasourceDict] = None,
        result_type: Optional[ChartDataResultType] = None,
        annotation_layers: Optional[List[Dict[str, Any]]] = None,
        applied_time_extras: Optional[Dict[str, str]] = None,
        apply_fetch_values_predicate: bool = False,
        granularity: Optional[str] = None,
        metrics: Optional[List[Metric]] = None,
        groupby: Optional[List[str]] = None,
        filters: Optional[List[QueryObjectFilterClause]] = None,
        time_range: Optional[str] = None,
        time_shift: Optional[str] = None,
        is_timeseries: Optional[bool] = None,
        timeseries_limit: int = 0,
        row_limit: Optional[int] = None,
        row_offset: Optional[int] = None,
        timeseries_limit_metric: Optional[Metric] = None,
        order_desc: bool = True,
        extras: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None,
        orderby: Optional[List[OrderBy]] = None,
        post_processing: Optional[List[Optional[Dict[str, Any]]]] = None,
        is_rowcount: bool = False,
        **kwargs: Any,
    ):
        """

        :param datasource: 数据源对象，可选。
        :param result_type: 返回结果类型 ChartDataResultType，可选。
        :param annotation_layers: 注释层（字典的列表），可选。
        :param applied_time_extras: 应用的自定义时间（字典的列表），可选。
        :param apply_fetch_values_predicate: 是否应用提取值判断。
        :param granularity: 时间粒度。
        :param metrics: 指标列表。
        :param groupby: 分组列名称的列表。
        :param filters: 过滤器 QueryObjectFilterClause 的列表。
        :param time_range: 时间范围。
        :param time_shift: 时间位移。
        :param is_timeseries: 是否时间序列。
        :param timeseries_limit: 时间序列限制。
        :param row_limit: 行限制。
        :param row_offset: 行位移。
        :param timeseries_limit_metric: 时间序列限制指标。
        :param order_desc: 是否降序。
        :param extras: 自定义数据。
        :param columns: 列集合。
        :param orderby: 排序列
        :param post_processing: 后处理。
        :param is_rowcount: 是否行计数。
        :param kwargs: 其它关键字参数。
        """

        columns = columns or []
        groupby = groupby or []
        extras = extras or {}
        annotation_layers = annotation_layers or []
        self.time_offsets = kwargs.get("time_offsets", [])
        self.inner_from_dttm = kwargs.get("inner_from_dttm")
        self.inner_to_dttm = kwargs.get("inner_to_dttm")

        self.is_rowcount = is_rowcount
        self.datasource = None
        if datasource:
            self.datasource = ConnectorRegistry.get_datasource(
                str(datasource["type"]), int(datasource["id"]), db.session
            )
        self.result_type = result_type
        self.apply_fetch_values_predicate = apply_fetch_values_predicate or False
        self.annotation_layers = [
            layer
            for layer in annotation_layers
            # formula annotations don't affect the payload, hence can be dropped
            if layer["annotationType"] != "FORMULA"
        ]
        self.applied_time_extras = applied_time_extras or {}
        self.granularity = granularity
        self.from_dttm, self.to_dttm = get_since_until(
            relative_start=extras.get(
                "relative_start", config["DEFAULT_RELATIVE_START_TIME"]
            ),
            relative_end=extras.get(
                "relative_end", config["DEFAULT_RELATIVE_END_TIME"]
            ),
            time_range=time_range,
            time_shift=time_shift,
        )
        # is_timeseries is True if time column is in either columns or groupby
        # (both are dimensions)
        self.is_timeseries = (
            is_timeseries
            if is_timeseries is not None
            else DTTM_ALIAS in columns + groupby
        )
        self.time_range = time_range
        self.time_shift = parse_human_timedelta(time_shift)
        self.post_processing = [
            post_proc for post_proc in post_processing or [] if post_proc
        ]

        # Support metric reference/definition in the format of
        #   1. 'metric_name'   - name of predefined metric
        #   2. { label: 'label_name' }  - legacy format for a predefined metric
        #   3. { expressionType: 'SIMPLE' | 'SQL', ... } - adhoc metric
        self.metrics = metrics and [
            x if isinstance(x, str) or is_adhoc_metric(x) else x["label"]
            for x in metrics
        ]

        self.row_limit = config["ROW_LIMIT"] if row_limit is None else row_limit
        self.row_offset = row_offset or 0
        self.filter = filters or []
        self.timeseries_limit = timeseries_limit
        self.timeseries_limit_metric = timeseries_limit_metric
        self.order_desc = order_desc
        self.extras = extras

        if config["SIP_15_ENABLED"]:
            self.extras["time_range_endpoints"] = get_time_range_endpoints(
                form_data=self.extras
            )

        self.columns = columns
        self.groupby = groupby or []
        self.orderby = orderby or []

        # rename deprecated fields
        for field in DEPRECATED_FIELDS:
            if field.old_name in kwargs:
                logger.warning(
                    "The field `%s` is deprecated, please use `%s` instead.",
                    field.old_name,
                    field.new_name,
                )
                value = kwargs[field.old_name]
                if value:
                    if hasattr(self, field.new_name):
                        logger.warning(
                            "The field `%s` is already populated, "
                            "replacing value with contents from `%s`.",
                            field.new_name,
                            field.old_name,
                        )
                    setattr(self, field.new_name, value)

        # move deprecated extras fields to extras
        for field in DEPRECATED_EXTRAS_FIELDS:
            if field.old_name in kwargs:
                logger.warning(
                    "The field `%s` is deprecated and should "
                    "be passed to `extras` via the `%s` property.",
                    field.old_name,
                    field.new_name,
                )
                value = kwargs[field.old_name]
                if value:
                    if hasattr(self.extras, field.new_name):
                        logger.warning(
                            "The field `%s` is already populated in "
                            "`extras`, replacing value with contents "
                            "from `%s`.",
                            field.new_name,
                            field.old_name,
                        )
                    self.extras[field.new_name] = value

    @property
    def metric_names(self) -> List[str]:
        """Return metrics names (labels), coerce adhoc metrics to strings."""
        return get_metric_names(self.metrics or [])

    @property
    def column_names(self) -> List[str]:
        """Return column names (labels). Reserved for future adhoc calculated
        columns."""
        return self.columns

    def validate(self, raise_exceptions: Optional[bool] = True) -> Optional[QueryObjectValidationError]:
        """Validate query object"""

        error: Optional[QueryObjectValidationError] = None
        all_labels = self.metric_names + self.column_names
        if len(set(all_labels)) < len(all_labels):
            dup_labels = find_duplicates(all_labels)
            error = QueryObjectValidationError(
                _(
                    "Duplicate column/metric labels: %(labels)s. Please make "
                    "sure all columns and metrics have a unique label.",
                    labels=", ".join(f'"{x}"' for x in dup_labels),
                )
            )
        if error and raise_exceptions:
            raise error
        return error

    def to_dict(self) -> Dict[str, Any]:
        """转换该对象为属性名称及其值的字典。"""

        query_object_dict = {
            "apply_fetch_values_predicate": self.apply_fetch_values_predicate,
            "granularity": self.granularity,
            "groupby": self.groupby,
            "from_dttm": self.from_dttm,
            "to_dttm": self.to_dttm,
            "inner_from_dttm": self.inner_from_dttm,
            "inner_to_dttm": self.inner_to_dttm,
            "is_rowcount": self.is_rowcount,
            "is_timeseries": self.is_timeseries,
            "metrics": self.metrics,
            "row_limit": self.row_limit,
            "row_offset": self.row_offset,
            "filter": self.filter,
            "timeseries_limit": self.timeseries_limit,
            "timeseries_limit_metric": self.timeseries_limit_metric,
            "order_desc": self.order_desc,
            "extras": self.extras,
            "columns": self.columns,
            "orderby": self.orderby,
        }
        return query_object_dict

    def cache_key(self, **extra: Any) -> str:
        """
        The cache key is made out of the key/values from to_dict(), plus any
        other key/values in `extra`
        We remove datetime bounds that are hard values, and replace them with
        the use-provided inputs to bounds, which may be time-relative (as in
        "5 days ago" or "now").
        """

        cache_dict = self.to_dict()
        cache_dict.update(extra)

        if not self.apply_fetch_values_predicate:
            del cache_dict["apply_fetch_values_predicate"]
        if self.datasource:
            cache_dict["datasource"] = self.datasource.uid
        if self.result_type:
            cache_dict["result_type"] = self.result_type
        if self.time_range:
            cache_dict["time_range"] = self.time_range
        if self.post_processing:
            cache_dict["post_processing"] = self.post_processing
        if self.time_offsets:
            cache_dict["time_offsets"] = self.time_offsets

        for k in ["from_dttm", "to_dttm"]:
            del cache_dict[k]

        annotation_fields = [
            "annotationType",
            "descriptionColumns",
            "intervalEndColumn",
            "name",
            "overrides",
            "sourceType",
            "timeColumn",
            "titleColumn",
            "value",
        ]
        annotation_layers = [
            {field: layer[field] for field in annotation_fields if field in layer}
            for layer in self.annotation_layers
        ]
        # only add to key if there are annotations present that affect the payload
        if annotation_layers:
            cache_dict["annotation_layers"] = annotation_layers

        return md5_sha_from_dict(cache_dict, default=json_int_dttm_ser, ignore_nan=True)

    def exec_post_processing(self, df: DataFrame) -> DataFrame:
        """
        对指定数据帧执行后处理操作（这些操作定义在 pandas_postprocessing 模块中）。

        :param df: DataFrame returned from database model.
        :return: new DataFrame to which all post processing operations have been
                 applied
        :raises QueryObjectValidationError: If the post processing operation
                 is incorrect
        """

        for post_process in self.post_processing:
            operation = post_process.get("operation")
            if not operation:
                raise QueryObjectValidationError(
                    _("`operation` property of post processing object undefined")
                )
            if not hasattr(pandas_postprocessing, operation):
                raise QueryObjectValidationError(
                    _(
                        "Unsupported post processing operation: %(operation)s",
                        type=operation,
                    )
                )
            options = post_process.get("options", {})
            df = getattr(pandas_postprocessing, operation)(df, **options)

        return df
