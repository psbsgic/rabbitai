# -*- coding: utf-8 -*-

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
    """查询 REST API视图模型，提供针对 `Query`对象关系模型的 API 操作功能。"""

    datamodel = SQLAInterface(Query)
    """对象关系模型访问接口"""
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
    """包含的路由方法名称集合"""
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
    """显示模型实例列表时要显示的列名称的列表"""
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
    """显示一个模型实例时要显示的列名称的列表"""
    base_filters = [["id", QueryFilter, lambda: []]]
    """基础过滤器列表"""
    base_order = ("changed_on", "desc")
    """基础排序"""
    openapi_spec_tag = "Queries"
    """开放API规范标签"""
    openapi_spec_methods = openapi_spec_methods_override
    """开放API规范方法"""

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
    """参与排序的列名称列表"""
    related_field_filters = {
        "created_by": RelatedFieldFilter("first_name", FilterRelatedOwners),
        "user": RelatedFieldFilter("first_name", FilterRelatedOwners),
    }
    """关联字段过滤器字典"""
    search_columns = ["changed_on", "database", "sql", "status", "user", "start_time"]
    """参与搜索的列名称列表"""
    filter_rel_fields = {"database": [["id", DatabaseFilter, lambda: []]]}
    """过滤器关联字段"""
    allowed_rel_fields = {"database", "user"}
    """允许的关联字段集合"""
    allowed_distinct_fields = {"status"}
    """允许的不同值字段集合"""
