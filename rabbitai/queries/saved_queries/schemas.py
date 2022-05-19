from marshmallow import fields, Schema
from marshmallow.validate import Length

openapi_spec_methods_override = {
    "get": {"get": {"description": "获取保存的查询",}},
    "get_list": {
        "get": {
            "description": "获取保存的查询列表，使用Rison或JSON查询参数进行过滤、排序、分页，以及选择特定的列和元数据。",
        }
    },
    "post": {"post": {"description": "创建保存的查询"}},
    "put": {"put": {"description": "更新保存的查询"}},
    "delete": {"delete": {"description": "删除保存的查询"}},
}
"""开放API规范方法架构"""
get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}
"""获取删除唯一标识列表架构"""
get_export_ids_schema = {"type": "array", "items": {"type": "integer"}}
"""获取导出唯一标识列表架构"""


class ImportV1SavedQuerySchema(Schema):
    """导入V1版本API保存查询架构，定义相关字段（schema、label、description、sql、uuid、version、database_uuid）及其类型"""

    schema = fields.String(allow_none=True, validate=Length(0, 128))
    label = fields.String(allow_none=True, validate=Length(0, 256))
    description = fields.String(allow_none=True)
    sql = fields.String(required=True)
    uuid = fields.UUID(required=True)
    version = fields.String(required=True)
    database_uuid = fields.UUID(required=True)
