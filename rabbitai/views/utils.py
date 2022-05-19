# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from datetime import date
from functools import wraps
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Set, Tuple, Union
from urllib import parse

import msgpack
import pyarrow as pa
import simplejson as json
from flask import g, request
from flask_appbuilder.security.sqla import models as ab_models
from flask_appbuilder.security.sqla.models import User
from flask_babel import _
from sqlalchemy.orm.exc import NoResultFound

import rabbitai.models.core as models
from rabbitai import app, dataframe, db, result_set, viz
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import (
    CacheLoadError,
    SerializationError,
    RabbitaiException,
    RabbitaiSecurityException,
)
from rabbitai.extensions import cache_manager, security_manager
from rabbitai.legacy import update_time_range
from rabbitai.models.core import Database
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice
from rabbitai.models.sql_lab import Query
from rabbitai.typing import FormData
from rabbitai.utils.core import QueryStatus, TimeRangeEndpoint
from rabbitai.utils.decorators import stats_timing
from rabbitai.viz import BaseViz

logger = logging.getLogger(__name__)
stats_logger = app.config["STATS_LOGGER"]


REJECTED_FORM_DATA_KEYS: List[str] = []
"""拒绝的表单数据键列表"""
if not app.config["ENABLE_JAVASCRIPT_CONTROLS"]:
    REJECTED_FORM_DATA_KEYS = ["js_tooltip", "js_onclick_href", "js_data_mutator"]


def bootstrap_user_data(user: User, include_perms: bool = False) -> Dict[str, Any]:
    """
    返回与指定用户相关的数据，并指定是否包括权限，默认不包括，这些数据将传递到客户端。

    - username
    - firstName
    - lastName
    - userId
    - isActive
    - createdOn
    - email
    - roles
    - permissions

    :param user: 用户对象。
    :param include_perms: 是否包括权限，默认False。
    :return:
    """

    if user.is_anonymous:
        payload = {}
        user.roles = (security_manager.find_role("Public"),)
    else:
        payload = {
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "userId": user.id,
            "isActive": user.is_active,
            "createdOn": user.created_on.isoformat(),
            "email": user.email,
        }

    if include_perms:
        roles, permissions = get_permissions(user)
        payload["roles"] = roles
        payload["permissions"] = permissions

    return payload


def get_permissions(user: User,) -> Tuple[Dict[str, List[List[str]]], DefaultDict[str, Set[str]]]:
    """
    获取指定用户的权限，返回角色列表和权限集合。

    :param user: 用户对象。
    :return: 角色列表和权限集合。
    """

    if not user.roles:
        raise AttributeError("User object does not have roles")

    roles = defaultdict(list)
    permissions = defaultdict(set)

    for role in user.roles:
        permissions_ = security_manager.get_role_permissions(role)
        for permission in permissions_:
            if permission[0] in ("datasource_access", "database_access"):
                permissions[permission[0]].add(permission[1])
            roles[role.name].append([permission[0], permission[1]])

    return roles, permissions


def get_viz(
    form_data: FormData,
    datasource_type: str,
    datasource_id: int,
    force: bool = False,
    force_cached: bool = False,
) -> BaseViz:
    """
    获取可视类型（BaseViz派生类型实例），
    首先，从表单数据中获取 viz_type 的值（即可视类型），据此获取可视类型，
    再依据数据源类型和标识（datasource_type, datasource_id）从数据库中获取数据源对象关系模型实例，
    构建可视类型新实例。

    :param form_data: 表单数据。
    :param datasource_type: 数据源类型。
    :param datasource_id: 数据源标识。
    :param force: 是否强制。
    :param force_cached: 是否强制缓存。
    :return: 可视类型（BaseViz派生类型实例）。
    """

    viz_type = form_data.get("viz_type", "table")
    datasource = ConnectorRegistry.get_datasource(datasource_type, datasource_id, db.session)
    viz_obj = viz.viz_types[viz_type](
        datasource, form_data=form_data, force=force, force_cached=force_cached
    )
    return viz_obj


def loads_request_json(request_json_data: str) -> Dict[Any, Any]:
    """
    加载（反序列化）指定请求Json字符串为Json对象。

    :param request_json_data: 请求Json格式字符串数据。
    :return: Json对象实例。
    """

    try:
        return json.loads(request_json_data)
    except (TypeError, json.JSONDecodeError):
        return {}


def get_form_data(
    slice_id: Optional[int] = None, use_slice_data: bool = False
) -> Tuple[Dict[str, Any], Optional[Slice]]:
    """
    从Web请求（request对象）中，获取指定切片的表单数据。
    这些数据来自 request.json["queries"]，request.form.["form_data"]，request.args.["form_data"]

    :param slice_id: 切片标识。
    :param use_slice_data: 是否使用切片数据。
    :return: 表单数据和切片模型实例，Tuple[Dict[str, Any], Optional[Slice]]。
    """

    form_data: Dict[str, Any] = {}
    # 图表数据 API 请求是 JSON
    request_json_data = (
        request.json["queries"][0]
        if request.is_json and "queries" in request.json
        else None
    )

    add_sqllab_custom_filters(form_data)

    request_form_data = request.form.get("form_data")
    request_args_data = request.args.get("form_data")
    if request_json_data:
        form_data.update(request_json_data)

    if request_form_data:
        parsed_form_data = loads_request_json(request_form_data)
        # 有些图表数据 API 请求是 form_data
        queries = parsed_form_data.get("queries")
        if isinstance(queries, list):
            form_data.update(queries[0])
        else:
            form_data.update(parsed_form_data)

    # 请求参数可以重写 body
    if request_args_data:
        form_data.update(loads_request_json(request_args_data))

    # Fallback to using the Flask globals (used for cache warm up) if defined.
    if not form_data and hasattr(g, "form_data"):
        form_data = getattr(g, "form_data")

    url_id = request.args.get("r")
    if url_id:
        saved_url = db.session.query(models.Url).filter_by(id=url_id).first()
        if saved_url:
            url_str = parse.unquote_plus(
                saved_url.url.split("?")[1][10:], encoding="utf-8"
            )
            url_form_data = loads_request_json(url_str)
            # allow form_date in request override saved url
            url_form_data.update(form_data)
            form_data = url_form_data

    form_data = {k: v for k, v in form_data.items() if k not in REJECTED_FORM_DATA_KEYS}

    # When a slice_id is present, load from DB and override
    # the form_data from the DB with the other form_data provided
    slice_id = form_data.get("slice_id") or slice_id
    slc = None

    # Check if form data only contains slice_id, additional filters and viz type
    valid_keys = ["slice_id", "extra_filters", "adhoc_filters", "viz_type"]
    valid_slice_id = all(key in valid_keys for key in form_data)

    # Include the slice_form_data if request from explore or slice calls
    # or if form_data only contains slice_id and additional filters
    if slice_id and (use_slice_data or valid_slice_id):
        slc = db.session.query(Slice).filter_by(id=slice_id).one_or_none()
        if slc:
            slice_form_data = slc.form_data.copy()
            slice_form_data.update(form_data)
            form_data = slice_form_data

    update_time_range(form_data)

    if app.config["SIP_15_ENABLED"]:
        form_data["time_range_endpoints"] = get_time_range_endpoints(
            form_data, slc, slice_id
        )

    return form_data, slc


def add_sqllab_custom_filters(form_data: Dict[Any, Any]) -> Any:
    """
    将 request.data 中的过滤器列表添加 SQLLab 自定义过滤器列表到指定表单数据。

    SQLLab 可以在 templateParams 中包括一个 "filters" 属性。
    该属性是要包括在请求中的过滤器列表。用于在SQLLab中测试模板。
    """

    try:
        data = json.loads(request.data)
        if isinstance(data, dict):
            params_str = data.get("templateParams")
            if isinstance(params_str, str):
                params = json.loads(params_str)
                if isinstance(params, dict):
                    filters = params.get("_filters")
                    if filters:
                        form_data.update({"filters": filters})
    except (TypeError, json.JSONDecodeError):
        data = {}


def get_datasource_info(
    datasource_id: Optional[int], datasource_type: Optional[str], form_data: FormData
) -> Tuple[int, Optional[str]]:
    """
    获取数据源信息（数据源标识和类型）。

    用于处理数据源信息的兼容层

    datasource_id & datasource_type 过去是在URL目录中传递的，现在它们应该是表单数据form_data的一部分，

    此函数允许在不复制代码的情况下同时支持这两种功能

    :param datasource_id: 数据源 ID，可选。
    :param datasource_type: 数据源类型，即 'druid' 或 'table'，可选。
    :param form_data: 表单数据

    :returns: 数据源 ID 和类型。

    :raises RabbitaiException: If the datasource no longer exists
    """

    datasource = form_data.get("datasource", "")

    if "__" in datasource:
        datasource_id, datasource_type = datasource.split("__")
        # The case where the datasource has been deleted
        if datasource_id == "None":
            datasource_id = None

    if not datasource_id:
        raise RabbitaiException(
            _("The dataset associated with this chart no longer exists")
        )

    datasource_id = int(datasource_id)

    return datasource_id, datasource_type


def apply_display_max_row_limit(
    sql_results: Dict[str, Any], rows: Optional[int] = None
) -> Dict[str, Any]:
    """
    给定 `sql_results` 嵌套结构, 对行数进行限制

    `sql_results` 是 来自sql_lab.get_sql_results 的嵌套结构，
    它包含查询相关元数据，以及由查询返回的数据集。
    该方法限制方法结果的行数，添加 `displayLimitReached: True` 标志到元数据中。

    :param sql_results: 来自 sql_lab.get_sql_results 的 SQL 查询结果。
    :returns: The mutated sql_results structure
    """

    display_limit = rows or app.config["DISPLAY_MAX_ROW"]

    if (
        display_limit
        and sql_results["status"] == QueryStatus.SUCCESS
        and display_limit < sql_results["query"]["rows"]
    ):
        sql_results["data"] = sql_results["data"][:display_limit]
        sql_results["displayLimitReached"] = True
    return sql_results


def get_time_range_endpoints(
    form_data: FormData, slc: Optional[Slice] = None, slice_id: Optional[int] = None
) -> Optional[Tuple[TimeRangeEndpoint, TimeRangeEndpoint]]:
    """
    Get the slice aware time range endpoints from the form-data falling back to the SQL
    database specific definition or default if not defined.

    Note under certain circumstances the slice object may not exist, however the slice
    ID may be defined which serves as a fallback.

    When SIP-15 is enabled all new slices will use the [start, end) interval. If the
    grace period is defined and has ended all slices will adhere to the [start, end)
    interval.

    :param form_data: The form-data
    :param slc: The slice
    :param slice_id: The slice ID
    :returns: The time range endpoints tuple
    """

    if (
        app.config["SIP_15_GRACE_PERIOD_END"]
        and date.today() >= app.config["SIP_15_GRACE_PERIOD_END"]
    ):
        return (TimeRangeEndpoint.INCLUSIVE, TimeRangeEndpoint.EXCLUSIVE)

    endpoints = form_data.get("time_range_endpoints")

    if (slc or slice_id) and not endpoints:
        try:
            _, datasource_type = get_datasource_info(None, None, form_data)
        except RabbitaiException:
            return None

        if datasource_type == "table":
            if not slc:
                slc = db.session.query(Slice).filter_by(id=slice_id).one_or_none()

            if slc and slc.datasource:
                endpoints = slc.datasource.database.get_extra().get(
                    "time_range_endpoints"
                )

            if not endpoints:
                endpoints = app.config["SIP_15_DEFAULT_TIME_RANGE_ENDPOINTS"]

    if endpoints:
        start, end = endpoints
        return (TimeRangeEndpoint(start), TimeRangeEndpoint(end))

    return (TimeRangeEndpoint.INCLUSIVE, TimeRangeEndpoint.EXCLUSIVE)


# /rabbitai-frontend/src/dashboard/util/componentTypes.js 中定义了所有组件类型。
CONTAINER_TYPES = ["COLUMN", "GRID", "TABS", "TAB", "ROW"]


def get_dashboard_extra_filters(slice_id: int, dashboard_id: int) -> List[Dict[str, Any]]:
    """
    获取仪表盘提供的额外过滤器。

    :param slice_id: 切片标识。
    :param dashboard_id: 仪表盘标识。
    :return:
    """

    session = db.session()
    dashboard = session.query(Dashboard).filter_by(id=dashboard_id).one_or_none()

    # is chart in this dashboard?
    if (
        dashboard is None
        or not dashboard.json_metadata
        or not dashboard.slices
        or not any([slc for slc in dashboard.slices if slc.id == slice_id])
    ):
        return []

    try:
        # does this dashboard have default filters?
        json_metadata = json.loads(dashboard.json_metadata)
        default_filters = json.loads(json_metadata.get("default_filters", "null"))
        if not default_filters:
            return []

        # 是否默认过滤器可应用于给定切片
        filter_scopes = json_metadata.get("filter_scopes", {})
        layout = json.loads(dashboard.position_json or "{}")

        if (
            isinstance(layout, dict)
            and isinstance(filter_scopes, dict)
            and isinstance(default_filters, dict)
        ):
            return build_extra_filters(layout, filter_scopes, default_filters, slice_id)
    except json.JSONDecodeError:
        pass

    return []


def build_extra_filters(
    layout: Dict[str, Dict[str, Any]],
    filter_scopes: Dict[str, Dict[str, Any]],
    default_filters: Dict[str, Dict[str, List[Any]]],
    slice_id: int,
) -> List[Dict[str, Any]]:
    """
    依据指定布局、过滤器范围、默认过滤器和切片标识，构建额外过滤器。

    :param layout: 布局，字典的字典。
    :param filter_scopes: 过滤器范围，字典的字典。
    :param default_filters: 默认过滤器，字典的字典。
    :param slice_id: 切片标识。

    :return: 字典的列表。
    """

    extra_filters = []

    # 如果图表不在过滤器范围内或图表不受过滤器影响，则不要应用过滤器。
    for filter_id, columns in default_filters.items():
        filter_slice = db.session.query(Slice).filter_by(id=filter_id).one_or_none()

        filter_configs: List[Dict[str, Any]] = []
        if filter_slice:
            filter_configs = (
                json.loads(filter_slice.params or "{}").get("filter_configs") or []
            )

        scopes_by_filter_field = filter_scopes.get(filter_id, {})
        for col, val in columns.items():
            if not val:
                continue

            current_field_scopes = scopes_by_filter_field.get(col, {})
            scoped_container_ids = current_field_scopes.get("scope", ["ROOT_ID"])
            immune_slice_ids = current_field_scopes.get("immune", [])

            for container_id in scoped_container_ids:
                if slice_id not in immune_slice_ids and is_slice_in_container(
                    layout, container_id, slice_id
                ):
                    # Ensure that the filter value encoding adheres to the filter select type.
                    for filter_config in filter_configs:
                        if filter_config["column"] == col:
                            is_multiple = filter_config["multiple"]

                            if not is_multiple and isinstance(val, list):
                                val = val[0]
                            elif is_multiple and not isinstance(val, list):
                                val = [val]
                            break

                    extra_filters.append(
                        {
                            "col": col,
                            "op": "in" if isinstance(val, list) else "==",
                            "val": val,
                        }
                    )

    return extra_filters


def is_slice_in_container(
    layout: Dict[str, Dict[str, Any]], container_id: str, slice_id: int
) -> bool:
    """
    指定切片是否在指定容器中。

    :param layout: 布局，容器标识和节点的字典。
    :param container_id: 容器标识。
    :param slice_id: 切片标识。
    :return:
    """

    if container_id == "ROOT_ID":
        return True

    node = layout[container_id]
    node_type = node.get("type")
    if node_type == "CHART" and node.get("meta", {}).get("chartId") == slice_id:
        return True

    if node_type in CONTAINER_TYPES:
        children = node.get("children", [])
        return any(
            is_slice_in_container(layout, child_id, slice_id) for child_id in children
        )

    return False


def is_owner(obj: Union[Dashboard, Slice], user: User) -> bool:
    """ Check if user is owner of the slice """
    return obj and user in obj.owners


def check_resource_permissions(check_perms: Callable[..., Any],) -> Callable[..., Any]:
    """用于使用传入函数检查请求权限的装饰程序。"""

    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            # check if the user can access the resource
            check_perms(*args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return decorator


def check_explore_cache_perms(_self: Any, cache_key: str) -> None:
    """
    Loads async explore_json request data from cache and performs access check

    :param _self: the Rabbitai view instance
    :param cache_key: the cache key passed into /explore_json/data/
    :raises RabbitaiSecurityException: If the user cannot access the resource
    """

    cached = cache_manager.cache.get(cache_key)
    if not cached:
        raise CacheLoadError("Cached data not found")

    check_datasource_perms(_self, form_data=cached["form_data"])


def check_datasource_perms(
    _self: Any,
    datasource_type: Optional[str] = None,
    datasource_id: Optional[int] = None,
    **kwargs: Any
) -> None:
    """
    Check if user can access a cached response from explore_json.

    This function takes `self` since it must have the same signature as the
    the decorated method.

    :param datasource_type: The datasource type, i.e., 'druid' or 'table'
    :param datasource_id: The datasource ID
    :raises RabbitaiSecurityException: If the user cannot access the resource
    """

    form_data = kwargs["form_data"] if "form_data" in kwargs else get_form_data()[0]

    try:
        datasource_id, datasource_type = get_datasource_info(
            datasource_id, datasource_type, form_data
        )
    except RabbitaiException as ex:
        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.FAILED_FETCHING_DATASOURCE_INFO_ERROR,
                level=ErrorLevel.ERROR,
                message=str(ex),
            )
        )

    if datasource_type is None:
        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.UNKNOWN_DATASOURCE_TYPE_ERROR,
                level=ErrorLevel.ERROR,
                message=_("Could not determine datasource type"),
            )
        )

    try:
        viz_obj = get_viz(
            datasource_type=datasource_type,
            datasource_id=datasource_id,
            form_data=form_data,
            force=False,
        )
    except NoResultFound:
        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.UNKNOWN_DATASOURCE_TYPE_ERROR,
                level=ErrorLevel.ERROR,
                message=_("Could not find viz object"),
            )
        )

    viz_obj.raise_for_access()


def check_slice_perms(_self: Any, slice_id: int) -> None:
    """
    Check if user can access a cached response from slice_json.

    This function takes `self` since it must have the same signature as the
    the decorated method.

    :param slice_id: The slice ID
    :raises RabbitaiSecurityException: If the user cannot access the resource
    """

    form_data, slc = get_form_data(slice_id, use_slice_data=True)

    if slc and slc.datasource:
        try:
            viz_obj = get_viz(
                datasource_type=slc.datasource.type,
                datasource_id=slc.datasource.id,
                form_data=form_data,
                force=False,
            )
        except NoResultFound:
            raise RabbitaiSecurityException(
                RabbitaiError(
                    error_type=RabbitaiErrorType.UNKNOWN_DATASOURCE_TYPE_ERROR,
                    level=ErrorLevel.ERROR,
                    message="Could not find viz object",
                )
            )

        viz_obj.raise_for_access()


def _deserialize_results_payload(
    payload: Union[bytes, str], query: Query, use_msgpack: Optional[bool] = False
) -> Dict[str, Any]:
    logger.debug("Deserializing from msgpack: %r", use_msgpack)
    if use_msgpack:
        with stats_timing(
            "sqllab.query.results_backend_msgpack_deserialize", stats_logger
        ):
            ds_payload = msgpack.loads(payload, raw=False)

        with stats_timing("sqllab.query.results_backend_pa_deserialize", stats_logger):
            try:
                pa_table = pa.deserialize(ds_payload["data"])
            except pa.ArrowSerializationError:
                raise SerializationError("Unable to deserialize table")

        df = result_set.RabbitaiResultSet.convert_table_to_df(pa_table)
        ds_payload["data"] = dataframe.df_to_records(df) or []

        db_engine_spec = query.database.db_engine_spec
        all_columns, data, expanded_columns = db_engine_spec.expand_data(
            ds_payload["selected_columns"], ds_payload["data"]
        )
        ds_payload.update(
            {"data": data, "columns": all_columns, "expanded_columns": expanded_columns}
        )

        return ds_payload

    with stats_timing("sqllab.query.results_backend_json_deserialize", stats_logger):
        return json.loads(payload)


def get_cta_schema_name(
    database: Database, user: ab_models.User, schema: str, sql: str
) -> Optional[str]:
    """
    基于应用的配置对象 SQLLAB_CTAS_SCHEMA_NAME_FUNC 属性提供的函数返回模式名称。

    :param database: 数据库对象模型
    :param user: 用户对象模型
    :param schema: 模式
    :param sql: SQL字符串。
    :return:
    """

    func: Optional[Callable[[Database, ab_models.User, str, str], str]] = app.config[
        "SQLLAB_CTAS_SCHEMA_NAME_FUNC"
    ]
    if not func:
        return None

    return func(database, user, schema, sql)
