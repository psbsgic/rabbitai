# RISON/JSON schemas for query parameters
from marshmallow import fields, Schema, validate

from rabbitai.charts.schemas import (
    datasource_name_description,
    datasource_type_description,
    datasource_uid_description,
)


class Datasource(Schema):
    """数据源架构。"""

    database_name = fields.String(description="数据库名称",)
    datasource_name = fields.String(description=datasource_name_description,)
    schema = fields.String(description="数据源结构",)
    datasource_type = fields.String(
        description=datasource_type_description,
        validate=validate.OneOf(choices=("druid", "table", "view")),
        required=True,
    )


class CacheInvalidationRequestSchema(Schema):
    """使缓存无效请求架构。"""

    datasource_uids = fields.List(fields.String(), description=datasource_uid_description,)
    datasources = fields.List(fields.Nested(Datasource), description="数据源和数据库名称的列表",)
