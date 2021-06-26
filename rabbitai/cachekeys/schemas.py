# RISON/JSON schemas for query parameters
from marshmallow import fields, Schema, validate

from rabbitai.charts.schemas import (
    datasource_name_description,
    datasource_type_description,
    datasource_uid_description,
)


class Datasource(Schema):
    database_name = fields.String(description="Datasource name",)
    datasource_name = fields.String(description=datasource_name_description,)
    schema = fields.String(description="Datasource schema",)
    datasource_type = fields.String(
        description=datasource_type_description,
        validate=validate.OneOf(choices=("druid", "table", "view")),
        required=True,
    )


class CacheInvalidationRequestSchema(Schema):
    datasource_uids = fields.List(
        fields.String(), description=datasource_uid_description,
    )
    datasources = fields.List(
        fields.Nested(Datasource),
        description="A list of the data source and database names",
    )
