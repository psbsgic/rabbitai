from typing import Any, Dict

from flask_babel import gettext as _
from marshmallow import EXCLUDE, fields, post_load, Schema, validate
from marshmallow.validate import Length, Range
from marshmallow_enum import EnumField

from rabbitai import app
from rabbitai.common.query_context import QueryContext
from rabbitai.db_engine_specs.base import builtin_time_grains
from rabbitai.utils import schema as utils
from rabbitai.utils.core import (
    AnnotationType,
    ChartDataResultFormat,
    ChartDataResultType,
    FilterOperator,
    PostProcessingBoxplotWhiskerType,
    PostProcessingContributionOrientation,
    TimeRangeEndpoint,
)

config = app.config

#
# RISON/JSON schemas for query parameters
#
get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}

width_height_schema = {
    "type": "array",
    "items": {"type": "integer"},
}
thumbnail_query_schema = {
    "type": "object",
    "properties": {"force": {"type": "boolean"}},
}
screenshot_query_schema = {
    "type": "object",
    "properties": {
        "force": {"type": "boolean"},
        "window_size": width_height_schema,
        "thumb_size": width_height_schema,
    },
}
get_export_ids_schema = {"type": "array", "items": {"type": "integer"}}

get_fav_star_ids_schema = {"type": "array", "items": {"type": "integer"}}

#
# Column schema descriptions
#
slice_name_description = "图表的名称。"
description_description = "图表的描述。"
viz_type_description = "图表可视化的类型。"
owners_description = (
    "所有者是允许删除或更改此图表的用户ID。"
    "如果留空，您将成为图表的所有者之一。"
)
params_description = (
    "在浏览视图中单击“保存”或“覆盖”按钮时，会动态生成参数。"
    "此JSON对象适用于可能希望更改特定参数的高级用户。"
)
query_context_description = (
    "查询上下文表示为生成可视化数据而需要运行的查询，以及应以何种格式返回数据。"
)
query_context_generation_description = (
    "查询上下文生成表示 query_context 是否由用户生成，以便它不会更新用户修改状态。"
)
cache_timeout_description = (
    "此图表的缓存超时持续时间（秒）。注意：如果未定义，则默认为数据源/表超时。"
)
datasource_id_description = (
    "此新图表将使用的数据集/数据源的id。"
    "完整的数据源标识需要 `datasouce_id`  和 `datasource_type`。"
)
datasource_uid_description = (
    "此新图表将使用的数据集/数据源的全局唯一标识（uid）。"
    "完整的数据源标识需要 `datasouce_uid` "
)
datasource_type_description = (
    "数据集/数据源的类型。"
)
datasource_name_description = "数据源名称。"
dashboards_description = "要包含此新图表的仪表板列表。"
changed_on_description = "上次更改图表的ISO日期。"
slice_url_description = "图表的访问地址 URL。"
form_data_description = (
    "来自用于形成图表数据查询的浏览控件的表单数据。"
)
description_markeddown_description = "图表说明的净化HTML版本。"
owners_name_description = "图表所有者的名称。"

#
# OpenAPI method specification overrides
#
openapi_spec_methods_override = {
    "get": {"get": {"description": "获取图表详细信息。"}},
    "get_list": {
        "get": {
            "description": "获取图表列表，使用Rison或JSON查询参数进行筛选、排序、分页以及选择特定列和元数据。",
        }
    },
    "info": {
        "get": {
            "description": "有关图表API端点的若干元数据信息。",
        }
    },
    "related": {
        "get": {
            "description": "获取图表所有可能所有者的列表。"
            "使用有 `column_name` 的 `owners` 参数。"
        }
    },
}


class ChartEntityResponseSchema(Schema):
    """图表对象响应结构。"""

    slice_id = fields.Integer()
    slice_name = fields.String(description=slice_name_description)
    cache_timeout = fields.Integer(description=cache_timeout_description)
    changed_on = fields.String(description=changed_on_description)
    modified = fields.String()
    datasource = fields.String(description=datasource_name_description)
    description = fields.String(description=description_description)
    description_markeddown = fields.String(description=description_markeddown_description)
    form_data = fields.Dict(description=form_data_description)
    slice_url = fields.String(description=slice_url_description)


class ChartPostSchema(Schema):
    """添加新图表的结构。"""

    slice_name = fields.String(
        description=slice_name_description, required=True, validate=Length(1, 250)
    )
    description = fields.String(description=description_description, allow_none=True)
    viz_type = fields.String(
        description=viz_type_description,
        validate=Length(0, 250),
        example=["bar", "line_multi", "area", "table"],
    )
    owners = fields.List(fields.Integer(description=owners_description))
    params = fields.String(
        description=params_description, allow_none=True, validate=utils.validate_json
    )
    query_context = fields.String(
        description=query_context_description,
        allow_none=True,
        validate=utils.validate_json,
    )
    query_context_generation = fields.Boolean(
        description=query_context_generation_description, allow_none=True
    )
    cache_timeout = fields.Integer(
        description=cache_timeout_description, allow_none=True
    )
    datasource_id = fields.Integer(description=datasource_id_description, required=True)
    datasource_type = fields.String(
        description=datasource_type_description,
        validate=validate.OneOf(choices=("druid", "table", "view")),
        required=True,
    )
    datasource_name = fields.String(
        description=datasource_name_description, allow_none=True
    )
    dashboards = fields.List(fields.Integer(description=dashboards_description))


class ChartPutSchema(Schema):
    """更新图表的结构。"""

    slice_name = fields.String(
        description=slice_name_description, allow_none=True, validate=Length(0, 250)
    )
    description = fields.String(description=description_description, allow_none=True)
    viz_type = fields.String(
        description=viz_type_description,
        allow_none=True,
        validate=Length(0, 250),
        example=["bar", "line_multi", "area", "table"],
    )
    owners = fields.List(fields.Integer(description=owners_description))
    params = fields.String(description=params_description, allow_none=True)
    query_context = fields.String(
        description=query_context_description, allow_none=True
    )
    query_context_generation = fields.Boolean(
        description=query_context_generation_description, allow_none=True
    )
    cache_timeout = fields.Integer(
        description=cache_timeout_description, allow_none=True
    )
    datasource_id = fields.Integer(
        description=datasource_id_description, allow_none=True
    )
    datasource_type = fields.String(
        description=datasource_type_description,
        validate=validate.OneOf(choices=("druid", "table", "view")),
        allow_none=True,
    )
    dashboards = fields.List(fields.Integer(description=dashboards_description))


class ChartGetDatasourceObjectDataResponseSchema(Schema):
    datasource_id = fields.Integer(description="数据源标识符")
    datasource_type = fields.Integer(description="数据源类型")


class ChartGetDatasourceObjectResponseSchema(Schema):
    label = fields.String(description="数据源的名称")
    value = fields.Nested(ChartGetDatasourceObjectDataResponseSchema)


class ChartGetDatasourceResponseSchema(Schema):
    count = fields.Integer(description="数据源的总数")
    result = fields.Nested(ChartGetDatasourceObjectResponseSchema)


class ChartCacheScreenshotResponseSchema(Schema):
    cache_key = fields.String(description="缓存键")
    chart_url = fields.String(description="用于呈现图表的url")
    image_url = fields.String(description="获取屏幕截图的url")


class ChartDataColumnSchema(Schema):
    column_name = fields.String(
        description="目标列的名称", example="mycol",
    )
    type = fields.String(description="目标列的类型", example="BIGINT")


class ChartDataAdhocMetricSchema(Schema):
    """
    Ad-hoc metrics are used to define metrics outside the datasource.
    """

    expressionType = fields.String(
        description="简单或 SQL指标",
        required=True,
        validate=validate.OneOf(choices=("SIMPLE", "SQL")),
        example="SQL",
    )
    aggregate = fields.String(
        description="聚合运算符。仅对于简单表达式类型是必需的。",
        validate=validate.OneOf(
            choices=("AVG", "COUNT", "COUNT_DISTINCT", "MAX", "MIN", "SUM")
        ),
    )
    column = fields.Nested(ChartDataColumnSchema)
    sqlExpression = fields.String(
        description="由SQL聚合表达式定义的指标。仅SQL表达式类型需要。",
        example="SUM(weight * observations) / SUM(weight)",
    )
    label = fields.String(
        description="指标的标签。除非hasCustomLabel为true，否则将自动生成，在这种情况下，必须定义标签。",
        example="Weighted observations",
    )
    hasCustomLabel = fields.Boolean(
        description="如果为false，将根据聚合表达式自动生成标签。如果为true，则必须指定自定义标签。",
        example=True,
    )
    optionName = fields.String(
        description="唯一标识符。可以是任何字符串值，只要所有指标都具有唯一标识符。如果未定义，将生成一个随机名称。",
        example="metric_aec60732-fac0-4b17-b736-93f1a5c93e30",
    )
    timeGrain = fields.String(
        description="时间过滤器的可选时间粒度", example="PT1M",
    )
    isExtra = fields.Boolean(
        description="指示过滤器是否由过滤器组件添加，而不是作为原始查询的一部分。"
    )


class ChartDataAggregateConfigField(fields.Dict):
    def __init__(self) -> None:
        super().__init__(
            description="键是要创建的聚合列的名称，值指定如何应用聚合的详细信息。"
            "如果运算符需要其他选项，可以将这些选项传递到此处，以便在运算符调用中解包。"
            "支持以下numpy运算符：average, argmin, argmax, cumsum, "
            "cumprod, max, mean, median, nansum, nanmin, nanmax, nanmean, nanmedian, "
            "min, percentile, prod, product, std, sum, var。"
            "运算符所需的任何选项都可以传递给 `options` 对象。\n"
            "\n"
            "在本例中，使用带有'q=0.25'参数的'percentile'运算符，基于'my_col'列中的值创建了一个新列'first_quantile'。",
            example={
                "first_quantile": {
                    "operator": "percentile",
                    "column": "my_col",
                    "options": {"q": 0.25},
                }
            },
        )


class ChartDataPostProcessingOperationOptionsSchema(Schema):
    pass


class ChartDataAggregateOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Aggregate operation config.
    """

    groupby = (
        fields.List(
            fields.String(
                allow_none=False, description="Columns by which to group by",
            ),
            minLength=1,
            required=True,
        ),
    )
    aggregates = ChartDataAggregateConfigField()


class ChartDataRollingOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Rolling operation config.
    """

    columns = (
        fields.Dict(
            description="要对其执行滚动的列，将源列映射到目标列。"
            "例如，`{'y': 'y'}` 将用 `y` 中的滚动值替换列 `y`，"
            "而 `{'y': 'y2'}` 将根据从`y`计算的滚动值添加一列 `y2` ，保留原始列`y`不变。",
            example={"weekly_rolling_sales": "sales"},
        ),
    )
    rolling_type = fields.String(
        description="滚动窗口的类型。任何numpy函数都可以工作。",
        validate=validate.OneOf(
            choices=(
                "average",
                "argmin",
                "argmax",
                "cumsum",
                "cumprod",
                "max",
                "mean",
                "median",
                "nansum",
                "nanmin",
                "nanmax",
                "nanmean",
                "nanmedian",
                "nanpercentile",
                "min",
                "percentile",
                "prod",
                "product",
                "std",
                "sum",
                "var",
            )
        ),
        required=True,
        example="percentile",
    )
    window = fields.Integer(
        description="滚动窗口的大小（以天为单位）。", required=True, example=7,
    )
    rolling_type_options = fields.Dict(
        desctiption="传递到滚动方法的可选选项。例如分位数运算所需。",
        example={},
    )
    center = fields.Boolean(
        description="标签应该在窗口的中心。默认：`false`",
        example=False,
    )
    win_type = fields.String(
        description="窗口函数的类型。详见"
        "[SciPy window functions](https://docs.scipy.org/doc/scipy/reference"
        "/signal.windows.html#module-scipy.signal.windows) ，"
        "有些窗口函数需要传递 "
        "附加参数到 `rolling_type_options`。例如，"
        "为了使用 `gaussian`, 需要提供参数 `std` 。",
        validate=validate.OneOf(
            choices=(
                "boxcar",
                "triang",
                "blackman",
                "hamming",
                "bartlett",
                "parzen",
                "bohman",
                "blackmanharris",
                "nuttall",
                "barthann",
                "kaiser",
                "gaussian",
                "general_gaussian",
                "slepian",
                "exponential",
            )
        ),
    )
    min_periods = fields.Integer(
        description="在结果集中包含的行所需的最小周期。",
        example=7,
    )


class ChartDataSelectOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Sort operation config.
    """

    columns = fields.List(
        fields.String(),
        description="按所需顺序从输入数据中选择的列。如果重命名了列，则应在此处引用原始列名。",
        example=["country", "gender", "age"],
    )
    exclude = fields.List(
        fields.String(),
        description="要从选择中排除的列。",
        example=["my_temp_column"],
    )
    rename = fields.List(
        fields.Dict(),
        description="要重命名的列，将源列映射到目标列。"
        "例如，`{'y': 'y2'}` 将命名列 `y` 为 `y2`。",
        example=[{"age": "average_age"}],
    )


class ChartDataSortOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Sort operation config.
    """

    columns = fields.Dict(
        description="要按其排序的列。键指定列名，值指定是否按升序排序。",
        example={"country": True, "gender": False},
        required=True,
    )
    aggregates = ChartDataAggregateConfigField()


class ChartDataContributionOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Contribution operation config.
    """

    orientation = fields.String(
        description="应跨行或列计算单元格值。",
        required=True,
        validate=validate.OneOf(
            choices=[val.value for val in PostProcessingContributionOrientation]
        ),
        example="row",
    )


class ChartDataProphetOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Prophet operation config.
    """

    time_grain = fields.String(
        description="用于在预测中指定时间段增量的时间粒度。"
        "支持 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) "
        "持续时间。",
        validate=validate.OneOf(
            choices=[
                i
                for i in {**builtin_time_grains, **config["TIME_GRAIN_ADDONS"]}.keys()
                if i
            ]
        ),
        example="P1D",
        required=True,
    )
    periods = fields.Integer(
        descrption="预测未来的时间段（以 `time_grain` 为单位）",
        min=1,
        example=7,
        required=True,
    )
    confidence_interval = fields.Float(
        description="预测置信区间宽度",
        validate=[
            Range(
                min=0,
                max=1,
                min_inclusive=False,
                max_inclusive=False,
                error=_("`confidence_interval` must be between 0 and 1 (exclusive)"),
            )
        ],
        example=0.8,
        required=True,
    )
    yearly_seasonality = fields.Raw(
        # TODO: add correct union type once supported by Marshmallow
        description="是否应采用年度季节性。"
        "整数值将指定季节性的傅立叶顺序，`None`将自动检测季节性。",
        example=False,
    )
    weekly_seasonality = fields.Raw(
        # TODO: add correct union type once supported by Marshmallow
        description="是否应采用周季节性。"
        "整数值将指定季节性的傅立叶顺序，`None`将自动检测季节性。",
        example=False,
    )
    monthly_seasonality = fields.Raw(
        # TODO: add correct union type once supported by Marshmallow
        description="是否应采用月季节性。"
        "整数值将指定季节性的傅立叶顺序，`None`将自动检测季节性。",
        example=False,
    )


class ChartDataBoxplotOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Boxplot operation config.
    """

    groupby = fields.List(
        fields.String(description="用于对查询进行分组的列。",),
        allow_none=True,
    )

    metrics = fields.List(
        fields.Raw(),
        description="聚合表达式。指标可以作为对数据源指标（字符串）的引用或仅在查询对象中定义的特殊指标传递。"
                    "有关特殊指标的结构，请参见 `ChartDataAdhocMetricSchema`",
    )

    whisker_type = fields.String(
        description="Whisker 类型，任何numpy函数都可以工作。",
        validate=validate.OneOf(
            choices=([val.value for val in PostProcessingBoxplotWhiskerType])
        ),
        required=True,
        example="tukey",
    )

    percentiles = fields.Tuple(
        (
            fields.Float(
                description="下百分位",
                validate=[
                    Range(
                        min=0,
                        max=100,
                        min_inclusive=False,
                        max_inclusive=False,
                        error=_(
                            "lower percentile must be greater than 0 and less "
                            "than 100. Must be lower than upper percentile."
                        ),
                    ),
                ],
            ),
            fields.Float(
                description="上百分位",
                validate=[
                    Range(
                        min=0,
                        max=100,
                        min_inclusive=False,
                        max_inclusive=False,
                        error=_(
                            "upper percentile must be greater than 0 and less "
                            "than 100. Must be higher than lower percentile."
                        ),
                    ),
                ],
            ),
        ),
        description="百分位类型的上百分位和下百分位。",
        example=[1, 99],
    )


class ChartDataPivotOptionsSchema(ChartDataPostProcessingOperationOptionsSchema):
    """
    Pivot operation config.
    """

    index = (
        fields.List(
            fields.String(
                allow_none=False,
                description="表索引上要分组的列（=行）",
            ),
            minLength=1,
            required=True,
        ),
    )
    columns = fields.List(
        fields.String(
            allow_none=False, description="表列上要分组的列",
        ),
    )
    metric_fill_value = fields.Number(
        description="用于将缺失值替换为聚合计算中的值。",
    )
    column_fill_value = fields.String(
        description="替换缺失透视表列名称的值。"
    )
    drop_missing_columns = fields.Boolean(
        description="不要包括其条目全部丢失的列(默认: `true`)。",
    )
    marginal_distributions = fields.Boolean(
        description="添加行/列的总计。(默认: `false`)",
    )
    marginal_distribution_name = fields.String(
        description="边际分布行/列的名称。(默认: `All`)",
    )
    aggregates = ChartDataAggregateConfigField()


class ChartDataGeohashDecodeOptionsSchema(
    ChartDataPostProcessingOperationOptionsSchema
):
    """
    Geohash decode operation config.
    """

    geohash = fields.String(
        description="包含geohash字符串的源列的名称", required=True,
    )
    latitude = fields.String(
        description="解码纬度的目标列的名称", required=True,
    )
    longitude = fields.String(
        description="解码经度的目标列的名称", required=True,
    )


class ChartDataGeohashEncodeOptionsSchema(
    ChartDataPostProcessingOperationOptionsSchema
):
    """
    Geohash encode operation config.
    """

    latitude = fields.String(
        description="源纬度列的名称", required=True,
    )
    longitude = fields.String(
        description="源经度列的名称", required=True,
    )
    geohash = fields.String(
        description="编码的geohash字符串的目标列的名称", required=True,
    )


class ChartDataGeodeticParseOptionsSchema(
    ChartDataPostProcessingOperationOptionsSchema
):
    """
    Geodetic point string parsing operation config.
    """

    geodetic = fields.String(
        description="包含大地测量点字符串的源列的名称",
        required=True,
    )
    latitude = fields.String(
        description="解码纬度的目标列的名称", required=True,
    )
    longitude = fields.String(
        description="解码经度的目标列的名称", required=True,
    )
    altitude = fields.String(
        description="解码高度的目标列的名称。如果省略，则忽略大地测量字符串中的高度信息。",
    )


class ChartDataPostProcessingOperationSchema(Schema):
    """图表数据后处理操作结构。"""

    operation = fields.String(
        description="后处理操作类型",
        required=True,
        validate=validate.OneOf(
            choices=(
                "aggregate",
                "boxplot",
                "contribution",
                "cum",
                "geodetic_parse",
                "geohash_decode",
                "geohash_encode",
                "pivot",
                "prophet",
                "rolling",
                "select",
                "sort",
                "diff",
                "compare",
            )
        ),
        example="aggregate",
    )
    options = fields.Dict(
        description="指定如何执行操作的选项。请参考相应的后处理操作选项架构。"
        "例如, `ChartDataPostProcessingOperationOptions` 指定透视表操作所需的选项。",
        example={
            "groupby": ["country", "gender"],
            "aggregates": {
                "age_q1": {
                    "operator": "percentile",
                    "column": "age",
                    "options": {"q": 0.25},
                },
                "age_mean": {"operator": "mean", "column": "age",},
            },
        },
    )


class ChartDataFilterSchema(Schema):
    col = fields.String(
        description="要过滤的列。", required=True, example="country"
    )
    op = fields.String(  # pylint: disable=invalid-name
        description="比较运算符。",
        validate=utils.OneOfCaseInsensitive(
            choices=[filter_op.value for filter_op in FilterOperator]
        ),
        required=True,
        example="IN",
    )
    val = fields.Raw(
        description="要比较的一个或多个值。可以是字符串、整数、十进制或列表，具体取决于运算符。",
        example=["China", "France", "Japan"],
    )
    grain = fields.String(
        description="时间过滤器的可选时间粒度", example="PT1M",
    )
    isExtra = fields.Boolean(
        description="指示过滤器是否由过滤器组件添加，而不是作为原始查询的一部分。"
    )


class ChartDataExtrasSchema(Schema):

    time_range_endpoints = fields.List(EnumField(TimeRangeEndpoint, by_value=True))
    relative_start = fields.String(
        description="相对时间增量的开始时间。"
        '默认: `config["DEFAULT_RELATIVE_START_TIME"]`',
        validate=validate.OneOf(choices=("today", "now")),
    )
    relative_end = fields.String(
        description="相对时间增量的结束时间。"
        '默认: `config["DEFAULT_RELATIVE_START_TIME"]`',
        validate=validate.OneOf(choices=("today", "now")),
    )
    where = fields.String(
        description="要使用AND运算符添加到查询的WHERE子句。",
    )
    having = fields.String(
        description="要使用AND运算符添加到聚合查询中的 HAVING 子句。",
    )
    having_druid = fields.List(
        fields.Nested(ChartDataFilterSchema),
        description="添加到传统的Druid数据源查询中的HAVING过滤器。",
    )
    time_grain_sqla = fields.String(
        description="时间列应该聚合到什么粒度级别。支持"
        "[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations)。",
        validate=validate.OneOf(
            choices=[
                i
                for i in {**builtin_time_grains, **config["TIME_GRAIN_ADDONS"]}.keys()
                if i
            ]
        ),
        example="P1D",
        allow_none=True,
    )
    druid_time_origin = fields.String(
        description="传统Druid数据源上时间粒度计数的起点。用于更改，例如：一周的第一天，周一/周日。",
        allow_none=True,
    )


class AnnotationLayerSchema(Schema):
    annotationType = fields.String(
        description="注释层的类型",
        validate=validate.OneOf(choices=[ann.value for ann in AnnotationType]),
    )
    color = fields.String(description="层颜色", allow_none=True,)
    descriptionColumns = fields.List(
        fields.String(),
        description="要用作说明的列。如果没有提供，将显示所有。",
    )
    hideLine = fields.Boolean(
        description="这条线应该是隐藏的。仅适用于线条批注",
        allow_none=True,
    )
    intervalEndColumn = fields.String(
        description=(
            "包含间隔结束的列。仅适用于间隔层"
        ),
        allow_none=True,
    )
    name = fields.String(description="层名称", required=True)
    opacity = fields.String(
        description="图层不透明度",
        validate=validate.OneOf(
            choices=("", "opacityLow", "opacityMedium", "opacityHigh"),
        ),
        allow_none=True,
        required=False,
    )
    overrides = fields.Dict(
        keys=fields.String(
            desciption="要重写的属性的名称",
            validate=validate.OneOf(
                choices=("granularity", "time_grain_sqla", "time_range", "time_shift"),
            ),
        ),
        values=fields.Raw(allow_none=True),
        description="哪些属性应该是可重写的",
        allow_none=True,
    )
    show = fields.Boolean(description="是否应该显示图层", required=True)
    showMarkers = fields.Boolean(
        description="是否应该显示标记。仅适用于线条批注。",
        required=True,
    )
    sourceType = fields.String(
        description="注释数据的源类型",
        validate=validate.OneOf(choices=("", "line", "NATIVE", "table",)),
    )
    style = fields.String(
        description="线条风格。仅适用于时间序列注释",
        validate=validate.OneOf(choices=("dashed", "dotted", "solid", "longDashed",)),
    )
    timeColumn = fields.String(
        description="具有事件日期或间隔开始日期的列", allow_none=True,
    )
    titleColumn = fields.String(description="列标题", allow_none=True,)
    width = fields.Float(
        description="注释线宽度",
        validate=[
            Range(
                min=0,
                min_inclusive=True,
                error=_("`width` must be greater or equal to 0"),
            )
        ],
    )
    value = fields.Raw(
        description="对于公式批注，其中包含公式。对于其他类型，这是源对象的主键。",
        required=True,
    )


class ChartDataDatasourceSchema(Schema):
    description = "图表数据源"
    id = fields.Integer(description="数据源标识", required=True,)
    type = fields.String(
        description="数据源类型",
        validate=validate.OneOf(choices=("druid", "table")),
    )


class ChartDataQueryObjectSchema(Schema):
    class Meta:  # pylint: disable=too-few-public-methods
        unknown = EXCLUDE

    datasource = fields.Nested(ChartDataDatasourceSchema, allow_none=True)
    result_type = EnumField(ChartDataResultType, by_value=True, allow_none=True)

    annotation_layers = fields.List(
        fields.Nested(AnnotationLayerSchema),
        description="要应用于图表的注释图层",
        allow_none=True,
    )
    applied_time_extras = fields.Dict(
        description="已应用于查询的临时外部对象的映射",
        allow_none=True,
        example={"__time_range": "1 year ago : now"},
    )
    apply_fetch_values_predicate = fields.Boolean(
        description="如果在数据源中定义了fetch values谓词（where子句），则将其添加到查询中",
        allow_none=True,
    )
    filters = fields.List(fields.Nested(ChartDataFilterSchema), allow_none=True)
    granularity = fields.String(
        description="用于时间过滤的时间列的名称。对于传统Druid 数据源，这定义了时间粒度。",
        allow_none=True,
    )
    granularity_sqla = fields.String(
        description="用于SQL数据源时间过滤的时态列的名称。此字段已弃用，请改用 `granularity` 。",
        allow_none=True,
        deprecated=True,
    )
    groupby = fields.List(
        fields.String(description="用于对查询进行分组的列。",),
        allow_none=True,
    )
    metrics = fields.List(
        fields.Raw(),
        description="聚合表达式。指标可以作为对数据源指标（字符串）的引用或仅在查询对象中定义的动态指标。"
        "动态指标结构详见 `ChartDataAdhocMetricSchema`。",
        allow_none=True,
    )
    post_processing = fields.List(
        fields.Nested(ChartDataPostProcessingOperationSchema, allow_none=True),
        allow_none=True,
        description="要应用于结果集的后处理操作。操作按顺序应用于结果集。",
    )
    time_range = fields.String(
        description="时间范围，表示为冒号分隔的字符串 `since : until` 或人类可读的自由格式。"
        "`since` 和 `until` 的有效格式：\n"
        "- ISO 8601\n"
        "- X days/years/hours/day/year/weeks\n"
        "- X days/years/hours/day/year/weeks ago\n"
        "- X days/years/hours/day/year/weeks from now\n"
        "\n"
        "此外，还可以使用以下自由形式：\n"
        "\n"
        "- Last day\n"
        "- Last week\n"
        "- Last month\n"
        "- Last quarter\n"
        "- Last year\n"
        "- No filter\n"
        "- Last X seconds/minutes/hours/days/weeks/months/years\n"
        "- Next X seconds/minutes/hours/days/weeks/months/years\n",
        example="Last week",
        allow_none=True,
    )
    time_shift = fields.String(
        description="人类可读的日期/时间字符串。"
        "有效值请参考 [parsdatetime](https://github.com/bear/parsedatetime) 。",
        allow_none=True,
    )
    is_timeseries = fields.Boolean(
        description="`query_object` 是否时间序列。", allow_none=True,
    )
    timeseries_limit = fields.Integer(
        description="时间序列查询的最大行数，默认：`0`",
        allow_none=True,
    )
    timeseries_limit_metric = fields.Raw(
        description="用于限制时间序列查询的指标。", allow_none=True,
    )
    row_limit = fields.Integer(
        description='最大行数(0=disabled). 默认: `config["ROW_LIMIT"]`',
        allow_none=True,
        validate=[
            Range(min=0, error=_("`row_limit` must be greater than or equal to 0"))
        ],
    )
    row_offset = fields.Integer(
        description="要跳过的行数。默认：`0`",
        allow_none=True,
        validate=[
            Range(min=0, error=_("`row_offset` must be greater than or equal to 0"))
        ],
    )
    order_desc = fields.Boolean(
        description="是否降序。默认: `false`", allow_none=True,
    )
    extras = fields.Nested(
        ChartDataExtrasSchema,
        description="要添加到查询的其它参数。",
        allow_none=True,
    )
    columns = fields.List(
        fields.String(),
        description="要在查询中选择的列。",
        allow_none=True,
    )
    orderby = fields.List(
        fields.Tuple(
            (
                fields.Raw(
                    validate=[
                        Length(min=1, error=_("orderby column must be populated"))
                    ],
                    allow_none=False,
                ),
                fields.Boolean(),
            )
        ),
        description="需要一个元组的列表，其中第一个元素是要排序的列名，第二个元素是布尔值。",
        allow_none=True,
        example=[("my_col_1", False), ("my_col_2", True)],
    )
    where = fields.String(
        description="要使用AND运算符添加到查询的WHERE子句。"
        "此字段已弃用，应传递给 `extras`。",
        allow_none=True,
        deprecated=True,
    )
    having = fields.String(
        description="要使用AND运算符添加到聚合查询的HAVING子句。"
        "此字段已弃用，应传递给 `extras`。",
        allow_none=True,
        deprecated=True,
    )
    having_filters = fields.List(
        fields.Nested(ChartDataFilterSchema),
        description="要添加到 Druid 数据源查询的 HAVING 过滤。"
        "此字段已弃用，应传递给 `extras`。",
        allow_none=True,
        deprecated=True,
    )
    druid_time_origin = fields.String(
        description="Druid 数据源上时间粒度计数的起点。"
        "此字段已弃用，应传递给 `extras`。",
        allow_none=True,
    )
    url_params = fields.Dict(
        description="传递到仪表板或浏览视图的可选查询参数",
        keys=fields.String(description="查询参数"),
        values=fields.String(description="查询参数的值"),
        allow_none=True,
    )
    is_rowcount = fields.Boolean(
        description="是否应返回实际查询的行数",
        allow_none=True,
    )
    time_offsets = fields.List(fields.String(), allow_none=True,)


class ChartDataQueryContextSchema(Schema):
    """图表数据查询上下文结构，定义图表数据查询上下文对象的字段和类型。"""

    datasource = fields.Nested(ChartDataDatasourceSchema)
    queries = fields.List(fields.Nested(ChartDataQueryObjectSchema))
    force = fields.Boolean(
        description="应该强制从源加载查询。默认: `false`",
    )

    result_type = EnumField(ChartDataResultType, by_value=True)
    result_format = EnumField(ChartDataResultFormat, by_value=True)

    @post_load
    def make_query_context(self, data: Dict[str, Any], **kwargs: Any) -> QueryContext:
        query_context = QueryContext(**data)
        return query_context


class AnnotationDataSchema(Schema):
    """注释数据结构。"""
    columns = fields.List(
        fields.String(),
        description="注释结果中可用的列",
        required=True,
    )
    records = fields.List(
        fields.Dict(keys=fields.String(),),
        description="将列名映射到其值的记录",
        required=True,
    )


class ChartDataResponseResult(Schema):
    """图表数据响应结果结构。"""
    annotation_data = fields.List(
        fields.Dict(
            keys=fields.String(description="注释层名称"),
            values=fields.String(),
        ),
        description="所有请求的注释数据",
        allow_none=True,
    )
    cache_key = fields.String(
        description="查询对象的唯一缓存键", required=True, allow_none=True,
    )
    cached_dttm = fields.String(
        description="缓存时间戳", required=True, allow_none=True,
    )
    cache_timeout = fields.Integer(
        description="缓存超时的顺序如下：自定义超时、数据源超时、默认配置超时。",
        required=True,
        allow_none=True,
    )
    error = fields.String(description="错误", allow_none=True,)
    is_cached = fields.Boolean(
        description="是否缓存结果", required=True, allow_none=None,
    )
    query = fields.String(
        description="已执行的查询语句", required=True, allow_none=False,
    )
    status = fields.String(
        description="查询状态",
        validate=validate.OneOf(
            choices=(
                "stopped",
                "failed",
                "pending",
                "running",
                "scheduled",
                "success",
                "timed_out",
            )
        ),
        allow_none=False,
    )
    stacktrace = fields.String(
        desciption="Stacktrace是否存在错误", allow_none=True,
    )
    rowcount = fields.Integer(
        description="结果集中的行数", allow_none=False,
    )
    data = fields.List(fields.Dict(), description="结果的列表")
    applied_filters = fields.List(
        fields.Dict(), description="应用的过滤器列表"
    )
    rejected_filters = fields.List(
        fields.Dict(), description="未使用的过滤器列表"
    )


class ChartDataResponseSchema(Schema):
    """图表数据响应结构。"""
    result = fields.List(
        fields.Nested(ChartDataResponseResult),
        description="A list of results for each corresponding query in the request.",
    )


class ChartDataAsyncResponseSchema(Schema):
    channel_id = fields.String(
        description="唯一会话异步通道ID", allow_none=False,
    )
    job_id = fields.String(description="唯一异步作业ID", allow_none=False,)
    user_id = fields.String(description="请求用户ID", allow_none=True,)
    status = fields.String(description="异步作业状态", allow_none=False,)
    result_url = fields.String(
        description="用于获取异步查询数据的唯一结果URL", allow_none=False,
    )


class ChartFavStarResponseResult(Schema):
    id = fields.Integer(description="图表标识")
    value = fields.Boolean(description="关注值")


class GetFavStarIdsSchema(Schema):
    result = fields.List(
        fields.Nested(ChartFavStarResponseResult),
        description="请求中每个对应图表的结果列表",
    )


class ImportV1ChartSchema(Schema):
    """导入V1图表结构。"""

    slice_name = fields.String(required=True)
    viz_type = fields.String(required=True)
    params = fields.Dict()
    query_context = fields.String(allow_none=True, validate=utils.validate_json)
    cache_timeout = fields.Integer(allow_none=True)
    uuid = fields.UUID(required=True)
    version = fields.String(required=True)
    dataset_uuid = fields.UUID(required=True)


CHART_SCHEMAS = (
    ChartDataQueryContextSchema,
    ChartDataResponseSchema,
    ChartDataAsyncResponseSchema,
    ChartDataAdhocMetricSchema,
    ChartDataAggregateOptionsSchema,
    ChartDataContributionOptionsSchema,
    ChartDataProphetOptionsSchema,
    ChartDataBoxplotOptionsSchema,
    ChartDataPivotOptionsSchema,
    ChartDataRollingOptionsSchema,
    ChartDataSelectOptionsSchema,
    ChartDataSortOptionsSchema,
    ChartDataGeohashDecodeOptionsSchema,
    ChartDataGeohashEncodeOptionsSchema,
    ChartDataGeodeticParseOptionsSchema,
    ChartEntityResponseSchema,
    ChartGetDatasourceResponseSchema,
    ChartCacheScreenshotResponseSchema,
    GetFavStarIdsSchema,
)
