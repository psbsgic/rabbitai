# -*- coding: utf-8 -*-

"""定义 SQL Lab 模板上下文"""

import json
import re
from functools import partial
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from flask import current_app, g, request
from flask_babel import gettext as _
from jinja2 import DebugUndefined
from jinja2.sandbox import SandboxedEnvironment
from typing_extensions import TypedDict

from rabbitai.exceptions import RabbitaiTemplateException
from rabbitai.extensions import feature_flag_manager
from rabbitai.utils.core import convert_legacy_filters_into_adhoc, merge_extra_filters
from rabbitai.utils.memoized import memoized

if TYPE_CHECKING:
    from rabbitai.connectors.sqla.models import SqlaTable
    from rabbitai.models.core import Database
    from rabbitai.models.sql_lab import Query

NONE_TYPE = type(None).__name__
ALLOWED_TYPES = (
    NONE_TYPE,
    "bool",
    "str",
    "unicode",
    "int",
    "long",
    "float",
    "list",
    "dict",
    "tuple",
    "set",
)
"""允许的基础类型名称的列表。"""
COLLECTION_TYPES = ("list", "dict", "tuple", "set")
"""集合类型名称的列表"""


@memoized
def context_addons() -> Dict[str, Any]:
    """从应用配置对象中获取 JINJA 模板上下文插件，缓存返回结果。"""
    return current_app.config.get("JINJA_CONTEXT_ADDONS", {})


class Filter(TypedDict):
    """过滤器，类型属性及其类型，col，op，val。"""

    op: str  # pylint: disable=C0103
    col: str
    val: Union[None, Any, List[Any]]


class ExtraCache:
    """Dummy 类，该类公开用于存储查询对象缓存键计算中使用的附加值的方法。"""

    # 用于检测是否存在可添加到缓存键的模板化方法的正则表达式。
    regex = re.compile(
        r"\{\{.*("
        r"current_user_id\(.*\)|"
        r"current_username\(.*\)|"
        r"cache_key_wrapper\(.*\)|"
        r"url_param\(.*\)"
        r").*\}\}"
    )

    def __init__(
        self,
        extra_cache_keys: Optional[List[Any]] = None,
        removed_filters: Optional[List[str]] = None,
    ):
        self.extra_cache_keys = extra_cache_keys
        self.removed_filters = removed_filters if removed_filters is not None else []

    def current_user_id(self, add_to_cache_keys: bool = True) -> Optional[int]:
        """
        返回当前已登录用户的唯一标识 ID。

        :param add_to_cache_keys: 是否该值要包括在缓存键中。
        :returns: 用户的唯一标识 ID。
        """

        if hasattr(g, "user") and g.user:
            if add_to_cache_keys:
                self.cache_key_wrapper(g.user.get_id())
            return g.user.get_id()
        return None

    def current_username(self, add_to_cache_keys: bool = True) -> Optional[str]:
        """
        返回当前已登录用户的用户名称。

        :param add_to_cache_keys: 是否该值要包括在缓存键中。
        :returns: 用户名称
        """

        if g.user and hasattr(g.user, "username"):
            if add_to_cache_keys:
                self.cache_key_wrapper(g.user.username)
            return g.user.username
        return None

    def cache_key_wrapper(self, key: Any) -> Any:
        """
        将值添加到用于计算缓存键的查询对象的列表中。

        如果以下情况适用，则需要这样做：
            - 已启用缓存
            - 查询是使用jinja模板动态生成的
            - `JINJA_CONTEXT_ADDONS` 或类似的内容用作查询中的过滤器

        :param key: 计算缓存键时应考虑的任何值
        :return: the original value ``key`` passed to the function
        """
        if self.extra_cache_keys is not None:
            self.extra_cache_keys.append(key)
        return key

    def url_param(
        self, param: str, default: Optional[str] = None, add_to_cache_keys: bool = True
    ) -> Optional[str]:
        """
        Read a url or post parameter and use it in your SQL Lab query.

        When in SQL Lab, it's possible to add arbitrary URL "query string" parameters,
        and use those in your SQL code. For instance you can alter your url and add
        `?foo=bar`, as in `{domain}/rabbitai/sqllab?foo=bar`. Then if your query is
        something like SELECT * FROM foo = '{{ url_param('foo') }}', it will be parsed
        at runtime and replaced by the value in the URL.

        As you create a visualization form this SQL Lab query, you can pass parameters
        in the explore view as well as from the dashboard, and it should carry through
        to your queries.

        Default values for URL parameters can be defined in chart metadata by adding the
        key-value pair `url_params: {'foo': 'bar'}`

        :param param: the parameter to lookup
        :param default: the value to return in the absence of the parameter
        :param add_to_cache_keys: Whether the value should be included in the cache key
        :returns: The URL parameters
        """

        from rabbitai.views.utils import get_form_data

        # 从Web请求参数中获取参数值
        if request.args.get(param):
            return request.args.get(param, default)

        # 从表单数据中获取参数值
        form_data, _ = get_form_data()
        url_params = form_data.get("url_params") or {}
        result = url_params.get(param, default)
        if add_to_cache_keys:
            self.cache_key_wrapper(result)
        return result

    def filter_values(
        self, column: str, default: Optional[str] = None, remove_filter: bool = False
    ) -> List[Any]:
        """Gets a values for a particular filter as a list

        This is useful if:
            - you want to use a filter component to filter a query where the name of
             filter component column doesn't match the one in the select statement
            - you want to have the ability for filter inside the main query for speed
            purposes

        Usage example::

            SELECT action, count(*) as times
            FROM logs
            WHERE
                action in ({{ "'" + "','".join(filter_values('action_type')) + "'" }})
            GROUP BY action

        :param column: column/filter name to lookup
        :param default: default value to return if there's no matching columns
        :param remove_filter: When set to true, mark the filter as processed,
            removing it from the outer query. Useful when a filter should
            only apply to the inner query
        :return: returns a list of filter values
        """

        return_val: List[Any] = []
        filters = self.get_filters(column, remove_filter)
        for flt in filters:
            val = flt.get("val")
            if isinstance(val, list):
                return_val.extend(val)
            elif val:
                return_val.append(val)

        if (not return_val) and default:
            # If no values are found, return the default provided.
            return_val = [default]

        return return_val

    def get_filters(self, column: str, remove_filter: bool = False) -> List[Filter]:
        """
        获取应用于指定列的过滤器。
        处理返回值列表外，类似 filter_values 函数。
        get_filters 函数返回在浏览UI中的运算符。

        非常适合以下情况：
            - 您想要处理的不仅仅是SQL子句中的IN运算符
            - 您希望为过滤器生成自定义SQL条件的操作
            - 为了提高速度，您希望在主查询中具有筛选功能

        示例::


            WITH RECURSIVE
                superiors(employee_id, manager_id, full_name, level, lineage) AS (
                SELECT
                    employee_id,
                    manager_id,
                    full_name,
                1 as level,
                employee_id as lineage
                FROM
                    employees
                WHERE
                1=1
                {# Render a blank line #}
                {%- for filter in get_filters('full_name', remove_filter=True) -%}
                {%- if filter.get('op') == 'IN' -%}
                    AND
                    full_name IN ( {{ "'" + "', '".join(filter.get('val')) + "'" }} )
                {%- endif -%}
                {%- if filter.get('op') == 'LIKE' -%}
                    AND
                    full_name LIKE {{ "'" + filter.get('val') + "'" }}
                {%- endif -%}
                {%- endfor -%}
                UNION ALL
                    SELECT
                        e.employee_id,
                        e.manager_id,
                        e.full_name,
                s.level + 1 as level,
                s.lineage
                    FROM
                        employees e,
                    superiors s
                    WHERE s.manager_id = e.employee_id
            )


            SELECT
                employee_id, manager_id, full_name, level, lineage
            FROM
                superiors
            order by lineage, level

        :param column: 要查找的列/过滤器名称
        :param remove_filter: 设置为true时，将过滤器标记为已处理，将其从外部查询中删除。当过滤器应仅应用于内部查询时，此选项非常有用
        :return: 过滤器的列表
        """

        from rabbitai.utils.core import FilterOperator
        from rabbitai.views.utils import get_form_data

        form_data, _ = get_form_data()
        convert_legacy_filters_into_adhoc(form_data)
        merge_extra_filters(form_data)

        filters: List[Filter] = []

        for flt in form_data.get("adhoc_filters", []):
            val: Union[Any, List[Any]] = flt.get("comparator")
            op: str = flt["operator"].upper() if "operator" in flt else None
            # fltOpName: str = flt.get("filterOptionName")
            if (
                flt.get("expressionType") == "SIMPLE"
                and flt.get("clause") == "WHERE"
                and flt.get("subject") == column
                and val
            ):
                if remove_filter:
                    if column not in self.removed_filters:
                        self.removed_filters.append(column)
                if op in (
                    FilterOperator.IN.value,
                    FilterOperator.NOT_IN.value,
                ) and not isinstance(val, list):
                    val = [val]

                filters.append({"op": op, "col": column, "val": val})

        return filters


def safe_proxy(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    安全调用指定函数。

    :param func: 要调用函数参数。
    :param args: 列表参数。
    :param kwargs: 关键字参数。
    :return:
    """

    return_value = func(*args, **kwargs)
    value_type = type(return_value).__name__
    if value_type not in ALLOWED_TYPES:
        raise RabbitaiTemplateException(
            _(
                "Unsafe return type for function %(func)s: %(value_type)s",
                func=func.__name__,
                value_type=value_type,
            )
        )
    if value_type in COLLECTION_TYPES:
        try:
            return_value = json.loads(json.dumps(return_value))
        except TypeError:
            raise RabbitaiTemplateException(
                _("Unsupported return value for method %(name)s", name=func.__name__, )
            )

    return return_value


def validate_context_types(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证指定上下文（字符串和任何值的字典）的值类型的有效性。

    :param context: 上下文（字符串和任何值的字典）。
    :return:
    """

    for key in context:
        arg_type = type(context[key]).__name__
        if arg_type not in ALLOWED_TYPES and key not in context_addons():
            if arg_type == "partial" and context[key].func.__name__ == "safe_proxy":
                continue
            raise RabbitaiTemplateException(
                _(
                    "Unsafe template value for key %(key)s: %(value_type)s",
                    key=key,
                    value_type=arg_type,
                )
            )
        if arg_type in COLLECTION_TYPES:
            try:
                context[key] = json.loads(json.dumps(context[key]))
            except TypeError:
                raise RabbitaiTemplateException(
                    _("Unsupported template value for key %(key)s", key=key)
                )

    return context


def validate_template_context(engine: Optional[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证模板上下文。

    :param engine:
    :param context:
    :return:
    """

    if engine and engine in context:
        # validate engine context separately to allow for engine-specific methods
        engine_context = validate_context_types(context.pop(engine))
        valid_context = validate_context_types(context)
        valid_context[engine] = engine_context
        return valid_context

    return validate_context_types(context)


class BaseTemplateProcessor:
    """特定于数据库的 jinja 上下文的基类"""

    engine: Optional[str] = None
    """数据库引擎名称"""

    def __init__(
        self,
        database: "Database",
        query: Optional["Query"] = None,
        table: Optional["SqlaTable"] = None,
        extra_cache_keys: Optional[List[Any]] = None,
        removed_filters: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        使用指定数据库模型对象、查询模型对象、SQL数据表对象、额外缓存键列表、移除的过滤器列表和其它关键字参数，创建新实例。

        :param database: 数据库模型对象。
        :param query: 查询模型对象。
        :param table: SQL数据表对象。
        :param extra_cache_keys: 额外缓存键列表。
        :param removed_filters: 移除的过滤器列表。
        :param kwargs: 关键字参数。
        """

        self._database = database
        self._query = query
        self._schema = None
        if query and query.schema:
            self._schema = query.schema
        elif table:
            self._schema = table.schema
        self._extra_cache_keys = extra_cache_keys
        self._removed_filters = removed_filters
        self._context: Dict[str, Any] = {}
        self._env = SandboxedEnvironment(undefined=DebugUndefined)
        self.set_context(**kwargs)

    def set_context(self, **kwargs: Any) -> None:
        """设置上下文，同时添加从配置对象中读取的上下文插件。"""
        self._context.update(kwargs)
        self._context.update(context_addons())

    def process_template(self, sql: str, **kwargs: Any) -> str:
        """处理SQL模板，使用上下文参数渲染SQL模板。

        >>> sql = "SELECT '{{ datetime(2017, 1, 1).isoformat() }}'"
        >>> process_template(sql)
        "SELECT '2017-01-01T00:00:00'"
        """

        template = self._env.from_string(sql)
        kwargs.update(self._context)

        context = validate_template_context(self.engine, kwargs)
        return template.render(context)


class JinjaTemplateProcessor(BaseTemplateProcessor):
    """
    Jinja模板处理器，使用上下文参数渲染模板。

    添加参数：url_param、current_user_id、current_username、cache_key_wrapper、filter_values、get_filters

    """

    def set_context(self, **kwargs: Any) -> None:
        """设置上下文，添加参数：url_param、current_user_id、current_username、cache_key_wrapper、filter_values、get_filters"""
        super().set_context(**kwargs)
        extra_cache = ExtraCache(self._extra_cache_keys, self._removed_filters)
        self._context.update(
            {
                "url_param": partial(safe_proxy, extra_cache.url_param),
                "current_user_id": partial(safe_proxy, extra_cache.current_user_id),
                "current_username": partial(safe_proxy, extra_cache.current_username),
                "cache_key_wrapper": partial(safe_proxy, extra_cache.cache_key_wrapper),
                "filter_values": partial(safe_proxy, extra_cache.filter_values),
                "get_filters": partial(safe_proxy, extra_cache.get_filters),
            }
        )


class NoOpTemplateProcessor(BaseTemplateProcessor):
    """原样返回模板的模板处理器。"""

    def process_template(self, sql: str, **kwargs: Any) -> str:
        """
        Makes processing a template a noop
        """
        return sql


class PrestoTemplateProcessor(JinjaTemplateProcessor):
    """Presto Jinja 上下文模板处理器。

    The methods described here are namespaced under ``presto`` in the
    jinja context as in ``SELECT '{{ presto.some_macro_call() }}'``
    """

    engine = "presto"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "first_latest_partition": partial(safe_proxy, self.first_latest_partition),
            "latest_partitions": partial(safe_proxy, self.latest_partitions),
            "latest_sub_partition": partial(safe_proxy, self.latest_sub_partition),
            "latest_partition": partial(safe_proxy, self.latest_partition),
        }

    @staticmethod
    def _schema_table(table_name: str, schema: Optional[str]) -> Tuple[str, Optional[str]]:
        if "." in table_name:
            schema, table_name = table_name.split(".")
        return table_name, schema

    def first_latest_partition(self, table_name: str) -> Optional[str]:
        """
        Gets the first value in the array of all latest partitions

        :param table_name: table name in the format `schema.table`
        :return: the first (or only) value in the latest partition array
        :raises IndexError: If no partition exists
        """

        latest_partitions = self.latest_partitions(table_name)
        return latest_partitions[0] if latest_partitions else None

    def latest_partitions(self, table_name: str) -> Optional[List[str]]:
        """
        Gets the array of all latest partitions

        :param table_name: table name in the format `schema.table`
        :return: the latest partition array
        """

        from rabbitai.db_engine_specs.presto import PrestoEngineSpec

        table_name, schema = self._schema_table(table_name, self._schema)
        return cast(PrestoEngineSpec, self._database.db_engine_spec).latest_partition(
            table_name, schema, self._database
        )[1]

    def latest_sub_partition(self, table_name: str, **kwargs: Any) -> Any:
        table_name, schema = self._schema_table(table_name, self._schema)

        from rabbitai.db_engine_specs.presto import PrestoEngineSpec

        return cast(
            PrestoEngineSpec, self._database.db_engine_spec
        ).latest_sub_partition(
            table_name=table_name, schema=schema, database=self._database, **kwargs
        )

    latest_partition = first_latest_partition


class HiveTemplateProcessor(PrestoTemplateProcessor):
    engine = "hive"


DEFAULT_PROCESSORS = {"presto": PrestoTemplateProcessor, "hive": HiveTemplateProcessor}
"""默认模板处理器字典，支持引擎：presto、hive。"""


@memoized
def get_template_processors() -> Dict[str, Any]:
    """返回模板处理器（引擎名称和模板处理器的字典）。"""
    processors = current_app.config.get("CUSTOM_TEMPLATE_PROCESSORS", {})
    for engine in DEFAULT_PROCESSORS:
        # do not overwrite engine-specific CUSTOM_TEMPLATE_PROCESSORS
        if not engine in processors:
            processors[engine] = DEFAULT_PROCESSORS[engine]

    return processors


def get_template_processor(
    database: "Database",
    table: Optional["SqlaTable"] = None,
    query: Optional["Query"] = None,
    **kwargs: Any,
) -> BaseTemplateProcessor:
    """
    获取模板处理器。

    :param database: 数据库对象。
    :param table: 数据表对象。
    :param query: 查询对象。
    :param kwargs:
    :return:
    """

    if feature_flag_manager.is_feature_enabled("ENABLE_TEMPLATE_PROCESSING"):
        template_processor = get_template_processors().get(
            database.backend, JinjaTemplateProcessor
        )
    else:
        template_processor = NoOpTemplateProcessor

    return template_processor(database=database, table=table, query=query, **kwargs)
