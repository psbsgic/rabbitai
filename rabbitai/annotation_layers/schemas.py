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

get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}

annotation_layer_name = "The annotation layer name"
annotation_layer_descr = "Give a description for this annotation layer"


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
