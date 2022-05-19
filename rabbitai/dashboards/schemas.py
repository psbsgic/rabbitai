import json
import re
from typing import Any, Dict, Union

from marshmallow import fields, post_load, Schema
from marshmallow.validate import Length, ValidationError

from rabbitai.exceptions import RabbitaiException
from rabbitai.utils import core as utils

get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}
get_export_ids_schema = {"type": "array", "items": {"type": "integer"}}
get_fav_star_ids_schema = {"type": "array", "items": {"type": "integer"}}
thumbnail_query_schema = {
    "type": "object",
    "properties": {"force": {"type": "boolean"}},
}

dashboard_title_description = "仪表盘标题。"
slug_description = "仪表板网址的唯一标识部分。"
owners_description = (
    "所有者是允许删除或更改此仪表板的用户ID。"
    "如果留空，您将成为仪表板的所有者之一。"
)
roles_description = (
    "角色是定义仪表板访问权限的列表。"
    "除了对数据集级访问的限制之外，还始终应用这些角色。"
    "如果未定义任何角色，则仪表板可供所有角色使用。"
)
position_json_description = (
    "此json对象描述小部件在仪表板中的位置。"
    "它是通过在仪表板视图中使用拖放来调整小部件大小和位置时动态生成的"
)
css_description = "仪表盘的重写 CSS。"
json_metadata_description = (
    "单击仪表板视图中的保存或覆盖按钮时，动态生成此JSON对象。"
    "这里公开它是为了供可能想要改变特定参数的超级用户引用。"
)
published_description = (
    "确定此仪表板在所有仪表板列表中是否可见。"
)
charts_description = (
    "仪表板图表的名称。名称用于遗留原因。"
)

openapi_spec_methods_override = {
    "get": {"get": {"description": "获取仪表板详细信息。"}},
    "get_list": {
        "get": {
            "description": "获取仪表板列表，使用Rison或JSON查询参数进行过滤、排序、分页以及选择特定列和元数据。",
        }
    },
    "info": {
        "get": {
            "description": "有关仪表板API端点的若干元数据信息。",
        }
    },
    "related": {
        "get": {"description": "获取仪表板所有可能拥有者的列表。"}
    },
}


def validate_json(value: Union[bytes, bytearray, str]) -> None:
    try:
        utils.validate_json(value)
    except RabbitaiException:
        raise ValidationError("JSON not valid")


def validate_json_metadata(value: Union[bytes, bytearray, str]) -> None:
    if not value:
        return
    try:
        value_obj = json.loads(value)
    except json.decoder.JSONDecodeError:
        raise ValidationError("JSON not valid")
    errors = DashboardJSONMetadataSchema().validate(value_obj, partial=False)
    if errors:
        raise ValidationError(errors)


class DashboardJSONMetadataSchema(Schema):
    show_native_filters = fields.Boolean()
    # native_filter_configuration is for dashboard-native filters
    native_filter_configuration = fields.List(fields.Dict(), allow_none=True)
    # chart_configuration for now keeps data about cross-filter scoping for charts
    chart_configuration = fields.Dict()
    # filter_sets_configuration is for dashboard-native filters
    filter_sets_configuration = fields.List(fields.Dict(), allow_none=True)
    timed_refresh_immune_slices = fields.List(fields.Integer())
    # deprecated wrt dashboard-native filters
    filter_scopes = fields.Dict()
    expanded_slices = fields.Dict()
    refresh_frequency = fields.Integer()
    # deprecated wrt dashboard-native filters
    default_filters = fields.Str()
    stagger_refresh = fields.Boolean()
    stagger_time = fields.Integer()
    color_scheme = fields.Str(allow_none=True)
    label_colors = fields.Dict()
    # used for v0 import/export
    import_time = fields.Integer()
    remote_id = fields.Integer()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class RolesSchema(Schema):
    id = fields.Int()
    name = fields.String()


class DashboardGetResponseSchema(Schema):
    id = fields.Int()
    slug = fields.String()
    url = fields.String()
    dashboard_title = fields.String(description=dashboard_title_description)
    thumbnail_url = fields.String()
    published = fields.Boolean()
    css = fields.String(description=css_description)
    json_metadata = fields.String(description=json_metadata_description)
    position_json = fields.String(description=position_json_description)
    changed_by_name = fields.String()
    changed_by_url = fields.String()
    changed_by = fields.Nested(UserSchema)
    changed_on = fields.DateTime()
    charts = fields.List(fields.String(description=charts_description))
    owners = fields.List(fields.Nested(UserSchema))
    roles = fields.List(fields.Nested(RolesSchema))
    table_names = fields.String()  # legacy nonsense
    changed_on_humanized = fields.String(data_key="changed_on_delta_humanized")


class DatabaseSchema(Schema):
    id = fields.Int()
    name = fields.String()
    backend = fields.String()
    allow_multi_schema_metadata_fetch = fields.Bool()  # pylint: disable=invalid-name
    allows_subquery = fields.Bool()
    allows_cost_estimate = fields.Bool()
    allows_virtual_table_explore = fields.Bool()
    explore_database_id = fields.Int()


class DashboardDatasetSchema(Schema):
    id = fields.Int()
    uid = fields.Str()
    column_formats = fields.Dict()
    database = fields.Nested(DatabaseSchema)
    default_endpoint = fields.String()
    filter_select = fields.Bool()
    filter_select_enabled = fields.Bool()
    is_sqllab_view = fields.Bool()
    name = fields.Str()
    datasource_name = fields.Str()
    table_name = fields.Str()
    type = fields.Str()
    schema = fields.Str()
    offset = fields.Int()
    cache_timeout = fields.Int()
    params = fields.Str()
    perm = fields.Str()
    edit_url = fields.Str()
    sql = fields.Str()
    select_star = fields.Str()
    main_dttm_col = fields.Str()
    health_check_message = fields.Str()
    fetch_values_predicate = fields.Str()
    template_params = fields.Str()
    owners = fields.List(fields.Int())
    columns = fields.List(fields.Dict())
    column_types = fields.List(fields.Int())
    metrics = fields.List(fields.Dict())
    order_by_choices = fields.List(fields.List(fields.Str()))
    verbose_map = fields.Dict(fields.Str(), fields.Str())
    time_grain_sqla = fields.List(fields.List(fields.Str()))
    granularity_sqla = fields.List(fields.List(fields.Str()))


class BaseDashboardSchema(Schema):
    # pylint: disable=no-self-use,unused-argument
    @post_load
    def post_load(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        if data.get("slug"):
            data["slug"] = data["slug"].strip()
            data["slug"] = data["slug"].replace(" ", "-")
            data["slug"] = re.sub(r"[^\w\-]+", "", data["slug"])
        return data

    # pylint: disable=no-self-use,unused-argument


class DashboardPostSchema(BaseDashboardSchema):
    dashboard_title = fields.String(
        description=dashboard_title_description,
        allow_none=True,
        validate=Length(0, 500),
    )
    slug = fields.String(
        description=slug_description, allow_none=True, validate=[Length(1, 255)]
    )
    owners = fields.List(fields.Integer(description=owners_description))
    roles = fields.List(fields.Integer(description=roles_description))
    position_json = fields.String(
        description=position_json_description, validate=validate_json
    )
    css = fields.String()
    json_metadata = fields.String(
        description=json_metadata_description, validate=validate_json_metadata,
    )
    published = fields.Boolean(description=published_description)


class DashboardPutSchema(BaseDashboardSchema):
    dashboard_title = fields.String(
        description=dashboard_title_description,
        allow_none=True,
        validate=Length(0, 500),
    )
    slug = fields.String(
        description=slug_description, allow_none=True, validate=Length(0, 255)
    )
    owners = fields.List(
        fields.Integer(description=owners_description, allow_none=True)
    )
    roles = fields.List(fields.Integer(description=roles_description, allow_none=True))
    position_json = fields.String(
        description=position_json_description, allow_none=True, validate=validate_json
    )
    css = fields.String(description=css_description, allow_none=True)
    json_metadata = fields.String(
        description=json_metadata_description,
        allow_none=True,
        validate=validate_json_metadata,
    )
    published = fields.Boolean(description=published_description, allow_none=True)


class ChartFavStarResponseResult(Schema):
    id = fields.Integer(description="图表标识")
    value = fields.Boolean(description="关注星级")


class GetFavStarIdsSchema(Schema):
    result = fields.List(
        fields.Nested(ChartFavStarResponseResult),
        description="请求中每个对应图表的结果列表",
    )


class ImportV1DashboardSchema(Schema):
    dashboard_title = fields.String(required=True)
    description = fields.String(allow_none=True)
    css = fields.String(allow_none=True)
    slug = fields.String(allow_none=True)
    uuid = fields.UUID(required=True)
    position = fields.Dict()
    metadata = fields.Dict()
    version = fields.String(required=True)
