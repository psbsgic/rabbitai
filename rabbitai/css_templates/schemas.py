openapi_spec_methods_override = {
    "get": {"get": {"description": "Get a CSS template"}},
    "get_list": {
        "get": {
            "description": "Get a list of CSS templates, use Rison or JSON "
            "query parameters for filtering, sorting,"
            " pagination and for selecting specific"
            " columns and metadata.",
        }
    },
    "post": {"post": {"description": "Create a CSS template"}},
    "put": {"put": {"description": "Update a CSS template"}},
    "delete": {"delete": {"description": "Delete CSS template"}},
}

get_delete_ids_schema = {"type": "array", "items": {"type": "integer"}}
