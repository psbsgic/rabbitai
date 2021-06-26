from marshmallow import fields, Schema
from marshmallow.validate import Length

openapi_spec_methods_override = {
    "get": {"get": {"description": "Get an Annotation layer"}},
    "get_list": {
        "get": {
            "description": "Get a list of Annotation layers, use Rison or JSON "
            "query parameters for filtering, sorting,"
            " pagination and for selecting specific"
            " columns and metadata.",
        }
    },
    "post": {"post": {"description": "Create an Annotation layer"}},
    "put": {"put": {"description": "Update an Annotation layer"}},
    "delete": {"delete": {"description": "Delete Annotation layer"}},
}
"""OpenAPI规范方法重写，Json格式字符串"""

get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}
"""获取删除标识的结构。"""

annotation_layer_name = "注释层名称"
annotation_layer_descr = "为该注释层给定描述信息"


class AnnotationLayerPostSchema(Schema):
    name = fields.String(
        description=annotation_layer_name, allow_none=False, validate=[Length(1, 250)]
    )
    descr = fields.String(description=annotation_layer_descr, allow_none=True)


class AnnotationLayerPutSchema(Schema):
    name = fields.String(
        description=annotation_layer_name, required=False, validate=[Length(1, 250)]
    )
    descr = fields.String(description=annotation_layer_descr, required=False)
