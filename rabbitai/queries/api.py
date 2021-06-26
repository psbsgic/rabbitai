import logging

from flask_appbuilder.models.sqla.interface import SQLAInterface

from rabbitai.constants import MODEL_API_RW_METHOD_PERMISSION_MAP, RouteMethod
from rabbitai.databases.filters import DatabaseFilter
from rabbitai.models.sql_lab import Query
from rabbitai.queries.filters import QueryFilter
from rabbitai.queries.schemas import openapi_spec_methods_override
from rabbitai.views.base_api import BaseRabbitaiModelRestApi, RelatedFieldFilter
from rabbitai.views.filters import FilterRelatedOwners

logger = logging.getLogger(__name__)


class QueryRestApi(BaseRabbitaiModelRestApi):
    datamodel = SQLAInterface(Query)

    resource_name = "query"

    class_permission_name = "Query"
    method_permission_name = MODEL_API_RW_METHOD_PERMISSION_MAP

    allow_browser_login = True
    include_route_methods = {
        RouteMethod.GET,
        RouteMethod.GET_LIST,
        RouteMethod.RELATED,
        RouteMethod.DISTINCT,
    }

    list_columns = [
        "id",
        "changed_on",
        "database.database_name",
        "executed_sql",
        "rows",
        "schema",
        "sql",
        "sql_tables",
        "status",
        "tab_name",
        "user.first_name",
        "user.id",
        "user.last_name",
        "user.username",
        "start_time",
        "end_time",
        "tmp_table_name",
        "tracking_url",
    ]
    show_columns = [
        "id",
        "changed_on",
        "client_id",
        "database.id",
        "end_result_backend_time",
        "end_time",
        "error_message",
        "executed_sql",
        "limit",
        "progress",
        "results_key",
        "rows",
        "schema",
        "select_as_cta",
        "select_as_cta_used",
        "select_sql",
        "sql",
        "sql_editor_id",
        "start_running_time",
        "start_time",
        "status",
        "tab_name",
        "tmp_schema_name",
        "tmp_table_name",
        "tracking_url",
    ]
    base_filters = [["id", QueryFilter, lambda: []]]
    base_order = ("changed_on", "desc")

    openapi_spec_tag = "Queries"
    openapi_spec_methods = openapi_spec_methods_override

    order_columns = [
        "changed_on",
        "database.database_name",
        "rows",
        "schema",
        "start_time",
        "sql",
        "tab_name",
        "user.first_name",
    ]

    related_field_filters = {
        "created_by": RelatedFieldFilter("first_name", FilterRelatedOwners),
        "user": RelatedFieldFilter("first_name", FilterRelatedOwners),
    }

    search_columns = ["changed_on", "database", "sql", "status", "user", "start_time"]

    filter_rel_fields = {"database": [["id", DatabaseFilter, lambda: []]]}
    allowed_rel_fields = {"database", "user"}
    allowed_distinct_fields = {"status"}
