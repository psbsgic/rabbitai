# -*- coding: utf-8 -*-

import json
import logging
import re
from contextlib import closing
from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Match,
    NamedTuple,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    TYPE_CHECKING,
    Union,
)

import pandas as pd
import sqlparse
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import current_app, g
from flask_babel import gettext as __, lazy_gettext as _
from marshmallow import fields, Schema
from marshmallow.validate import Range
from sqlalchemy import column, select, types
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.interfaces import Compiled, Dialect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.engine.url import make_url, URL
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.sql import quoted_name, text
from sqlalchemy.sql.expression import ColumnClause, Select, TextAsFrom
from sqlalchemy.types import String, TypeEngine, UnicodeText
from typing_extensions import TypedDict

from rabbitai import security_manager, sql_parse
from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.models.sql_lab import Query
from rabbitai.models.sql_types.base import literal_dttm_type_factory
from rabbitai.sql_parse import ParsedQuery, Table
from rabbitai.utils import core as utils
from rabbitai.utils.core import ColumnSpec, GenericDataType
from rabbitai.utils.hashing import md5_sha_from_str
from rabbitai.utils.memoized import memoized
from rabbitai.utils.network import is_hostname_valid, is_port_open

if TYPE_CHECKING:
    # prevent circular imports
    from rabbitai.connectors.sqla.models import TableColumn
    from rabbitai.models.core import Database

logger = logging.getLogger()


class TimeGrain(NamedTuple):
    """时间刻度对象，包括：name、label、function、duration。"""

    name: str
    label: str
    function: str
    duration: Optional[str]


QueryStatus = utils.QueryStatus
"""查询状态枚举。"""

builtin_time_grains: Dict[Optional[str], str] = {
    None: __("Original value"),
    "PT1S": __("Second"),
    "PT5S": __("5 second"),
    "PT30S": __("30 second"),
    "PT1M": __("Minute"),
    "PT5M": __("5 minute"),
    "PT10M": __("10 minute"),
    "PT15M": __("15 minute"),
    "PT0.5H": __("Half hour"),
    "PT1H": __("Hour"),
    "PT6H": __("6 hour"),
    "P1D": __("Day"),
    "P1W": __("Week"),
    "P1M": __("Month"),
    "P0.25Y": __("Quarter"),
    "P1Y": __("Year"),
    "1969-12-28T00:00:00Z/P1W": __("Week starting Sunday"),
    "1969-12-29T00:00:00Z/P1W": __("Week starting Monday"),
    "P1W/1970-01-03T00:00:00Z": __("Week ending Saturday"),
    "P1W/1970-01-04T00:00:00Z": __("Week_ending Sunday"),
}
"""在建的时间刻度字典，时间刻度名称和显示名称。"""


class TimestampExpression(ColumnClause):
    """时间戳表达式，列从句。"""

    def __init__(self, expr: str, col: ColumnClause, **kwargs: Any) -> None:
        """Sqlalchemy class that can be used to render native column elements
        respeting engine-specific quoting rules as part of a string-based expression.

        :param expr: Sql expression with '{col}' denoting the locations where the col
        object will be rendered.
        :param col: the target column
        """
        super().__init__(expr, **kwargs)
        self.col = col

    @property
    def _constructor(self) -> ColumnClause:
        # Needed to ensure that the column label is rendered correctly when
        # proxied to the outer query.
        # See https://github.com/sqlalchemy/sqlalchemy/issues/4730
        return ColumnClause


@compiles(TimestampExpression)
def compile_timegrain_expression(
    element: TimestampExpression, compiler: Compiled, **kwargs: Any
) -> str:
    """
    编译时间粒度表达式。

    :param element: 时间戳表达式。
    :param compiler: 编译器。
    :param kwargs:
    :return:
    """
    return element.name.replace("{col}", compiler.process(element.col, **kwargs))


class LimitMethod:
    """枚举可以应用限制的方式"""

    FETCH_MANY = "fetch_many"
    WRAP_SQL = "wrap_sql"
    FORCE_LIMIT = "force_limit"


class BaseEngineSpec:
    """
    数据库引擎特定配置的抽象类。

    - allows_alias_to_source_column: 当SELECT中的列具有与源列相同的别名时，引擎是否能够为ORDER BY中使用的聚合子句选择源列。
    - allows_hidden_orderby_agg: 引擎是否允许ORDER BY直接使用聚合子句，而不必在SELECT中添加相同的聚合。
    """

    # region 字段声明

    engine = "base"  # str as defined in sqlalchemy.engine.engine
    """
    引擎，定义在 sqlalchemy.engine.engine 中的字符串。
    SQLAlchemy 是通过 Engine 来驱动，Engine 维护了一个连接池（Pool）对象和方言（Dialect）
    """
    engine_aliases: Set[str] = set()
    """数据库引擎别名集合。"""
    engine_name: Optional[str] = None  # used for user messages, overridden in child classes
    """引擎名称。用于用户消息，在子类中重写"""

    _date_trunc_functions: Dict[str, str] = {}
    """日期截断函数字典。"""
    _time_grain_expressions: Dict[Optional[str], str] = {}
    """时间刻度表达式字典。"""

    column_type_mappings: Tuple[
        Tuple[
            Pattern[str],
            Union[TypeEngine, Callable[[Match[str]], TypeEngine]],
            GenericDataType,
        ],
        ...,
    ] = (
        (
            re.compile(r"^smallint", re.IGNORECASE),
            types.SmallInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^int.*", re.IGNORECASE),
            types.Integer(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^bigint", re.IGNORECASE),
            types.BigInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^decimal", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^numeric", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (re.compile(r"^float", re.IGNORECASE), types.Float(), GenericDataType.NUMERIC,),
        (
            re.compile(r"^double", re.IGNORECASE),
            types.Float(),
            GenericDataType.NUMERIC,
        ),
        (re.compile(r"^real", re.IGNORECASE), types.REAL, GenericDataType.NUMERIC,),
        (
            re.compile(r"^smallserial", re.IGNORECASE),
            types.SmallInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^serial", re.IGNORECASE),
            types.Integer(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^bigserial", re.IGNORECASE),
            types.BigInteger(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^money", re.IGNORECASE),
            types.Numeric(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^string", re.IGNORECASE),
            types.String(),
            utils.GenericDataType.STRING,
        ),
        (
            re.compile(r"^N((VAR)?CHAR|TEXT)", re.IGNORECASE),
            UnicodeText(),
            utils.GenericDataType.STRING,
        ),
        (
            re.compile(r"^((VAR)?CHAR|TEXT|STRING)", re.IGNORECASE),
            String(),
            utils.GenericDataType.STRING,
        ),
        (
            re.compile(r"^((TINY|MEDIUM|LONG)?TEXT)", re.IGNORECASE),
            String(),
            utils.GenericDataType.STRING,
        ),
        (re.compile(r"^LONG", re.IGNORECASE), types.Float(), GenericDataType.NUMERIC,),
        (
            re.compile(r"^datetime", re.IGNORECASE),
            types.DateTime(),
            GenericDataType.TEMPORAL,
        ),
        (re.compile(r"^date", re.IGNORECASE), types.Date(), GenericDataType.TEMPORAL,),
        (
            re.compile(r"^timestamp", re.IGNORECASE),
            types.TIMESTAMP(),
            GenericDataType.TEMPORAL,
        ),
        (
            re.compile(r"^interval", re.IGNORECASE),
            types.Interval(),
            GenericDataType.TEMPORAL,
        ),
        (re.compile(r"^time", re.IGNORECASE), types.Time(), GenericDataType.TEMPORAL,),
        (
            re.compile(r"^bool.*", re.IGNORECASE),
            types.Boolean(),
            GenericDataType.BOOLEAN,
        ),
    )
    """列数据类型映射，匹配样式、数据库数据类型、通用（适合前端和后端的）数据类型组成元组的元组。"""

    time_groupby_inline = False
    """是否内联时间分组"""
    limit_method = LimitMethod.FORCE_LIMIT
    """限制方法"""
    time_secondary_columns = False
    """是否第二时间列"""
    allows_joins = True
    """是否允许连接"""
    allows_subqueries = True
    """是否允许子查询"""
    allows_alias_in_select = True
    """是否允许在SELECT语句中使用别名"""
    allows_alias_in_orderby = True
    """是否允许在ORDER BY语句中使用别名"""
    allows_sql_comments = True
    """是否允许SQL注释"""
    allows_alias_to_source_column = True
    """ORDER BY子句是否可以使用在SELECT中创建的与源列相同的别名"""
    allows_hidden_ordeby_agg = True
    """ORDERBY子句是否必须出现在SELECT中，如果为TRUE，则不必出现。"""
    force_column_alias_quotes = False
    """是否强制列别名界定"""
    arraysize = 0
    """数组大小"""
    max_column_name_length = 0
    """最大列名称长度"""
    try_remove_schema_from_table_name = True
    """是否尝试从数据表名称中移除模式"""
    run_multiple_statements_as_one = False
    """是否将多个语句作为一个语句来运行"""
    custom_errors: Dict[
        Pattern[str], Tuple[str, RabbitaiErrorType, Dict[str, Any]]
    ] = {}
    """自定义错误字典"""

    # endregion

    @classmethod
    def get_dbapi_exception_mapping(cls) -> Dict[Type[Exception], Type[Exception]]:
        """
        获取数据库API异常映射（字典）。

        每个引擎都可以实现自己的特定异常并将其聚合为RabbitAI DBAPI异常。

        :return: 驱动程序特定异常到 RabbitAI 自定义异常的映射。
        """
        return {}

    @classmethod
    def get_dbapi_mapped_exception(cls, exception: Exception) -> Exception:
        """
        从特定于驱动程序的异常中获取 RabbitAI 自定义DBAPI异常。

        如果引擎需要对异常执行额外更改，例如更改异常消息或实现自定义更复杂的逻辑，则重写

        :param exception: T驱动程序的异常
        :return: 自定义DBAPI异常。
        """
        new_exception = cls.get_dbapi_exception_mapping().get(type(exception))
        if not new_exception:
            return exception
        return new_exception(str(exception))

    @classmethod
    def get_allow_cost_estimate(cls, extra: Dict[str, Any]) -> bool:
        """
        返回一个布尔值指示是否允许进行耗时评估。

        :param extra:
        :return:
        """
        return False

    @classmethod
    def get_engine(
        cls,
        database: "Database",
        schema: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Engine:
        """
        获取指定数据库的数据库引擎。

        :param database: 数据库模型对象。
        :param schema: 模式。
        :param source: 查询源。
        :return: 数据库引擎 Engine。
        """

        user_name = utils.get_username()
        return database.get_sqla_engine(
            schema=schema, nullpool=True, user_name=user_name, source=source
        )

    @classmethod
    def get_timestamp_expr(
        cls,
        col: ColumnClause,
        pdf: Optional[str],
        time_grain: Optional[str],
        type_: Optional[str] = None,
    ) -> TimestampExpression:
        """
        构造要在SQLAlchemy查询中使用的时间戳表达式。

        :param col: TimestampExpression 的目标列。
        :param pdf: 日期格式(seconds or milliseconds)
        :param time_grain: 时间刻度，如：P1Y 表示1年
        :param type_: 列类型。

        :return: TimestampExpression 实例。
        """

        if time_grain:
            time_expr = cls.get_time_grain_expressions().get(time_grain)
            if not time_expr:
                raise NotImplementedError(
                    f"No grain spec for {time_grain} for database {cls.engine}"
                )
            if type_ and "{func}" in time_expr:
                date_trunc_function = cls._date_trunc_functions.get(type_)
                if date_trunc_function:
                    time_expr = time_expr.replace("{func}", date_trunc_function)
            if type_ and "{type}" in time_expr:
                date_trunc_function = cls._date_trunc_functions.get(type_)
                if date_trunc_function:
                    time_expr = time_expr.replace("{type}", type_)
        else:
            time_expr = "{col}"

        # if epoch, translate to DATE using db specific conf
        if pdf == "epoch_s":
            time_expr = time_expr.replace("{col}", cls.epoch_to_dttm())
        elif pdf == "epoch_ms":
            time_expr = time_expr.replace("{col}", cls.epoch_ms_to_dttm())

        return TimestampExpression(time_expr, col, type_=col.type)

    @classmethod
    def get_time_grains(cls) -> Tuple[TimeGrain, ...]:
        """
        生成支持的时间粒度的元组。

        :return: 引擎支持的所有时间粒度。
        """

        ret_list = []
        time_grains = builtin_time_grains.copy()
        time_grains.update(current_app.config["TIME_GRAIN_ADDONS"])
        for duration, func in cls.get_time_grain_expressions().items():
            if duration in time_grains:
                name = time_grains[duration]
                ret_list.append(TimeGrain(name, _(name), func, duration))
        return tuple(ret_list)

    @classmethod
    def _sort_time_grains(cls, val: Tuple[Optional[str], str], index: int) -> Union[float, int, str]:
        """
        Return an ordered time-based value of a portion of a time grain
        for sorting
        Values are expected to be either None or start with P or PT
        Have a numerical value in the middle and end with
        a value for the time interval
        It can also start or end with epoch start time denoting a range
        i.e, week beginning or ending with a day
        """

        pos = {
            "FIRST": 0,
            "SECOND": 1,
            "THIRD": 2,
            "LAST": 3,
        }

        if val[0] is None:
            return pos["FIRST"]

        prog = re.compile(r"(.*\/)?(P|PT)([0-9\.]+)(S|M|H|D|W|M|Y)(\/.*)?")
        result = prog.match(val[0])

        # for any time grains that don't match the format, put them at the end
        if result is None:
            return pos["LAST"]

        second_minute_hour = ["S", "M", "H"]
        day_week_month_year = ["D", "W", "M", "Y"]
        is_less_than_day = result.group(2) == "PT"
        interval = result.group(4)
        epoch_time_start_string = result.group(1) or result.group(5)
        has_starting_or_ending = bool(len(epoch_time_start_string or ""))

        def sort_day_week() -> int:
            if has_starting_or_ending:
                return pos["LAST"]
            if is_less_than_day:
                return pos["SECOND"]
            return pos["THIRD"]

        def sort_interval() -> float:
            if is_less_than_day:
                return second_minute_hour.index(interval)
            return day_week_month_year.index(interval)

        # 0: all "PT" values should come before "P" values (i.e, PT10M)
        # 1: order values within the above arrays ("D" before "W")
        # 2: sort by numeric value (PT10M before PT15M)
        # 3: sort by any week starting/ending values
        plist = {
            0: sort_day_week(),
            1: pos["SECOND"] if is_less_than_day else pos["THIRD"],
            2: sort_interval(),
            3: float(result.group(3)),
        }

        return plist.get(index, 0)

    @classmethod
    def get_time_grain_expressions(cls) -> Dict[Optional[str], str]:
        """
        返回所有支持的时间粒度的字典，包括任何可能已添加的粒度，但不包括配置文件中任何可能禁用的粒度。

        应用配置对象中的 TIME_GRAIN_ADDON_EXPRESSIONS 和 TIME_GRAIN_DENYLIST 分别设置要添加和禁用的时间粒度。

        :return: 引擎支持的所有时间粒度表达式。
        """

        time_grain_expressions = cls._time_grain_expressions.copy()
        grain_addon_expressions = current_app.config["TIME_GRAIN_ADDON_EXPRESSIONS"]
        time_grain_expressions.update(grain_addon_expressions.get(cls.engine, {}))
        denylist: List[str] = current_app.config["TIME_GRAIN_DENYLIST"]
        for key in denylist:
            time_grain_expressions.pop(key)

        return dict(
            sorted(
                time_grain_expressions.items(),
                key=lambda x: (
                    cls._sort_time_grains(x, 0),
                    cls._sort_time_grains(x, 1),
                    cls._sort_time_grains(x, 2),
                    cls._sort_time_grains(x, 3),
                ),
            )
        )

    @classmethod
    def fetch_data(cls, cursor: Any, limit: Optional[int] = None) -> List[Tuple[Any, ...]]:
        """
        依据指定游标实例，从数据库中提取数据，返回元组的列表。

        :param cursor: 游标实例。
        :param limit: 游标返回的最大行数。
        :return: 查询结果。
        """

        if cls.arraysize:
            cursor.arraysize = cls.arraysize
        try:
            if cls.limit_method == LimitMethod.FETCH_MANY and limit:
                return cursor.fetchmany(limit)
            return cursor.fetchall()
        except Exception as ex:
            raise cls.get_dbapi_mapped_exception(ex)

    @classmethod
    def expand_data(
        cls, columns: List[Dict[Any, Any]], data: List[Dict[Any, Any]]
    ) -> Tuple[List[Dict[Any, Any]], List[Dict[Any, Any]], List[Dict[Any, Any]]]:
        """
        有些引擎支持扩展嵌套字段。有关详细信息，请参见Presto spec中的实现。

        :param columns: columns selected in the query
        :param data: original data set
        :return: list of all columns(selected columns and their nested fields),
                 expanded data set, listed of nested fields
        """
        return columns, data, []

    @classmethod
    def alter_new_orm_column(cls, orm_col: "TableColumn") -> None:
        """Allow altering default column attributes when first detected/added

        For instance special column like `__time` for Druid can be
        set to is_dttm=True. Note that this only gets called when new
        columns are detected/created"""

    @classmethod
    def epoch_to_dttm(cls) -> str:
        """
        将纪元（秒）转换为可在查询中使用的日期时间的SQL表达式。
        在返回表达式中，引用列应表示为 `{col}`，例如 "FROM_UNIXTIME({col})"

        :return: SQL表达式。
        """
        raise NotImplementedError()

    @classmethod
    def epoch_ms_to_dttm(cls) -> str:
        """
        将纪元（毫秒）转换为可在查询中使用的日期时间的SQL表达式。

        :return: SQL表达式。
        """
        return cls.epoch_to_dttm().replace("{col}", "({col}/1000)")

    @classmethod
    def get_datatype(cls, type_code: Any) -> Optional[str]:
        """
        将列类型代码从游标描述更改为字符串表示。

        :param type_code: 游标描述的类型代码。
        :return: 类型代码的字符串表示。
        """
        if isinstance(type_code, str) and type_code != "":
            return type_code.upper()
        return None

    @classmethod
    def normalize_indexes(cls, indexes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        规范化索引，以提高数据库引擎之间的一致性。

        默认情况下为noop

        :param indexes: SQLAlchemy返回的原始索引。
        :return: 更清晰、更一致的索引定义。
        """
        return indexes

    @classmethod
    def extra_table_metadata(
        cls, database: "Database", table_name: str, schema_name: str
    ) -> Dict[str, Any]:
        """
        返回特定于引擎的数据表元数据。

        :param database: 数据库模型对象。
        :param table_name: 数据表名称。
        :param schema_name: 模式名称。
        :return: 特定于引擎的数据表元数据。
        """

        return {}

    @classmethod
    def apply_limit_to_sql(
        cls, sql: str, limit: int, database: "Database", force: bool = False
    ) -> str:
        """
        更改SQL语句以应用LIMIT子句

        :param sql: SQL 查询字符串。
        :param limit: 查询返回的最大行数
        :param database: 数据库模型对象。
        :return: 带 LIMIT子句 的 SQL 查询字符串。
        """

        if cls.limit_method == LimitMethod.WRAP_SQL:
            sql = sql.strip("\t\n ;")
            qry = (
                select("*")
                .select_from(TextAsFrom(text(sql), ["*"]).alias("inner_qry"))
                .limit(limit)
            )
            return database.compile_sqla_query(qry)

        if cls.limit_method == LimitMethod.FORCE_LIMIT:
            parsed_query = sql_parse.ParsedQuery(sql)
            sql = parsed_query.set_or_update_query_limit(limit, force=force)

        return sql

    @classmethod
    def get_limit_from_sql(cls, sql: str) -> Optional[int]:
        """
        从指定SQL查询字符串中提取限制（查询返回的最大行数）。

        :param sql: SQL查询字符串。
        :return: 限制（查询返回的最大行数）。
        """
        parsed_query = sql_parse.ParsedQuery(sql)
        return parsed_query.limit

    @classmethod
    def set_or_update_query_limit(cls, sql: str, limit: int) -> str:
        """
        基于原始查询创建查询，但使用新的limit子句。

        :param sql: SQL query
        :param limit: New limit to insert/replace into query
        :return: Query with new limit
        """
        parsed_query = sql_parse.ParsedQuery(sql)
        return parsed_query.set_or_update_query_limit(limit)

    @classmethod
    def df_to_sql(
        cls,
        database: "Database",
        table: Table,
        df: pd.DataFrame,
        to_sql_kwargs: Dict[str, Any],
    ) -> None:
        """
        Upload data from a Pandas DataFrame to a database.

        For regular engines this calls the `pandas.DataFrame.to_sql` method. Can be
        overridden for engines that don't work well with this method, e.g. Hive and
        BigQuery.

        Note this method does not create metadata for the table.

        :param database: The database to upload the data to
        :param table: The table to upload the data to
        :param df: The dataframe with data to be uploaded
        :param to_sql_kwargs: The kwargs to be passed to pandas.DataFrame.to_sql` method
        """

        engine = cls.get_engine(database)
        to_sql_kwargs["name"] = table.table

        if table.schema:
            # Only add schema when it is preset and non empty.
            to_sql_kwargs["schema"] = table.schema

        if engine.dialect.supports_multivalues_insert:
            to_sql_kwargs["method"] = "multi"

        df.to_sql(con=engine, **to_sql_kwargs)

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        """
        Convert Python datetime object to a SQL expression

        :param target_type: The target type of expression
        :param dttm: The datetime object
        :return: The SQL expression
        """
        return None

    @classmethod
    def get_all_datasource_names(cls, database: "Database", datasource_type: str) -> List[utils.DatasourceName]:
        """
        Returns a list of all tables or views in database.

        :param database: Database instance
        :param datasource_type: Datasource_type can be 'table' or 'view'
        :return: List of all datasources in database or schema
        """

        schemas = database.get_all_schema_names(
            cache=database.schema_cache_enabled,
            cache_timeout=database.schema_cache_timeout,
            force=True,
        )
        all_datasources: List[utils.DatasourceName] = []
        for schema in schemas:
            if datasource_type == "table":
                all_datasources += database.get_all_table_names_in_schema(
                    schema=schema,
                    force=True,
                    cache=database.table_cache_enabled,
                    cache_timeout=database.table_cache_timeout,
                )
            elif datasource_type == "view":
                all_datasources += database.get_all_view_names_in_schema(
                    schema=schema,
                    force=True,
                    cache=database.table_cache_enabled,
                    cache_timeout=database.table_cache_timeout,
                )
            else:
                raise Exception(f"Unsupported datasource_type: {datasource_type}")
        return all_datasources

    @classmethod
    def handle_cursor(cls, cursor: Any, query: Query, session: Session) -> None:
        """Handle a live cursor between the execute and fetchall calls

        The flow works without this method doing anything, but it allows
        for handling the cursor and updating progress information in the
        query object"""

    @classmethod
    def extract_error_message(cls, ex: Exception) -> str:
        return f"{cls.engine} error: {cls._extract_error_message(ex)}"

    @classmethod
    def _extract_error_message(cls, ex: Exception) -> str:
        """Extract error message for queries"""
        return utils.error_msg_from_exception(ex)

    @classmethod
    def extract_errors(
        cls, ex: Exception, context: Optional[Dict[str, Any]] = None
    ) -> List[RabbitaiError]:
        raw_message = cls._extract_error_message(ex)

        context = context or {}
        for regex, (message, error_type, extra) in cls.custom_errors.items():
            match = regex.search(raw_message)
            if match:
                params = {**context, **match.groupdict()}
                extra["engine_name"] = cls.engine_name
                return [
                    RabbitaiError(
                        error_type=error_type,
                        message=message % params,
                        level=ErrorLevel.ERROR,
                        extra=extra,
                    )
                ]

        return [
            RabbitaiError(
                error_type=RabbitaiErrorType.GENERIC_DB_ENGINE_ERROR,
                message=cls._extract_error_message(ex),
                level=ErrorLevel.ERROR,
                extra={"engine_name": cls.engine_name},
            )
        ]

    @classmethod
    def adjust_database_uri(cls, uri: URL, selected_schema: Optional[str]) -> None:
        """
        Mutate the database component of the SQLAlchemy URI.

        The URI here represents the URI as entered when saving the database,
        ``selected_schema`` is the schema currently active presumably in
        the SQL Lab dropdown. Based on that, for some database engine,
        we can return a new altered URI that connects straight to the
        active schema, meaning the users won't have to prefix the object
        names by the schema name.

        Some databases engines have 2 level of namespacing: database and
        schema (postgres, oracle, mssql, ...)
        For those it's probably better to not alter the database
        component of the URI with the schema name, it won't work.

        Some database drivers like presto accept '{catalog}/{schema}' in
        the database component of the URL, that can be handled here.
        """

    @classmethod
    def patch(cls) -> None:
        """"""

    @classmethod
    def get_schema_names(cls, inspector: Inspector) -> List[str]:
        """
        Get all schemas from database

        :param inspector: SqlAlchemy inspector
        :return: All schemas in the database
        """
        return sorted(inspector.get_schema_names())

    @classmethod
    def get_table_names(
        cls, database: "Database", inspector: Inspector, schema: Optional[str]
    ) -> List[str]:
        """
        Get all tables from schema

        :param database: database
        :param inspector: SqlAlchemy inspector
        :param schema: Schema to inspect. If omitted, uses default schema for database
        :return: All tables in schema
        """

        tables = inspector.get_table_names(schema)
        if schema and cls.try_remove_schema_from_table_name:
            tables = [re.sub(f"^{schema}\\.", "", table) for table in tables]
        return sorted(tables)

    @classmethod
    def get_view_names(
        cls, database: "Database", inspector: Inspector, schema: Optional[str]
    ) -> List[str]:
        """
        Get all views from schema

        :param database: database
        :param inspector: SqlAlchemy inspector
        :param schema: Schema name. If omitted, uses default schema for database
        :return: All views in schema
        """
        views = inspector.get_view_names(schema)
        if schema and cls.try_remove_schema_from_table_name:
            views = [re.sub(f"^{schema}\\.", "", view) for view in views]
        return sorted(views)

    @classmethod
    def get_table_comment(
        cls, inspector: Inspector, table_name: str, schema: Optional[str]
    ) -> Optional[str]:
        """
        Get comment of table from a given schema and table

        :param inspector: SqlAlchemy Inspector instance
        :param table_name: Table name
        :param schema: Schema name. If omitted, uses default schema for database
        :return: comment of table
        """

        comment = None
        try:
            comment = inspector.get_table_comment(table_name, schema)
            comment = comment.get("text") if isinstance(comment, dict) else None
        except NotImplementedError:
            # It's expected that some dialects don't implement the comment method
            pass
        except Exception as ex:
            logger.error("Unexpected error while fetching table comment", exc_info=True)
            logger.exception(ex)
        return comment

    @classmethod
    def get_columns(
        cls, inspector: Inspector, table_name: str, schema: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Get all columns from a given schema and table

        :param inspector: SqlAlchemy Inspector instance
        :param table_name: Table name
        :param schema: Schema name. If omitted, uses default schema for database
        :return: All columns in table
        """
        return inspector.get_columns(table_name, schema)

    @classmethod
    def where_latest_partition(
        cls,
        table_name: str,
        schema: Optional[str],
        database: "Database",
        query: Select,
        columns: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[Select]:
        """
        Add a where clause to a query to reference only the most recent partition

        :param table_name: Table name
        :param schema: Schema name
        :param database: Database instance
        :param query: SqlAlchemy query
        :param columns: List of TableColumns
        :return: SqlAlchemy query with additional where clause referencing latest
        partition
        """

        return None

    @classmethod
    def _get_fields(cls, cols: List[Dict[str, Any]]) -> List[Any]:
        return [column(c["name"]) for c in cols]

    @classmethod
    def select_star(
        cls,
        database: "Database",
        table_name: str,
        engine: Engine,
        schema: Optional[str] = None,
        limit: int = 100,
        show_cols: bool = False,
        indent: bool = True,
        latest_partition: bool = True,
        cols: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Generate a "SELECT * from [schema.]table_name" query with appropriate limit.

        WARNING: expects only unquoted table and schema names.

        :param database: Database instance
        :param table_name: Table name, unquoted
        :param engine: SqlALchemy Engine instance
        :param schema: Schema, unquoted
        :param limit: limit to impose on query
        :param show_cols: Show columns in query; otherwise use "*"
        :param indent: Add indentation to query
        :param latest_partition: Only query latest partition
        :param cols: Columns to include in query
        :return: SQL query
        """

        fields: Union[str, List[Any]] = "*"
        cols = cols or []
        if (show_cols or latest_partition) and not cols:
            cols = database.get_columns(table_name, schema)

        if show_cols:
            fields = cls._get_fields(cols)
        quote = engine.dialect.identifier_preparer.quote
        if schema:
            full_table_name = quote(schema) + "." + quote(table_name)
        else:
            full_table_name = quote(table_name)

        qry = select(fields).select_from(text(full_table_name))

        if limit:
            qry = qry.limit(limit)
        if latest_partition:
            partition_query = cls.where_latest_partition(
                table_name, schema, database, qry, columns=cols
            )
            if partition_query is not None:
                qry = partition_query
        sql = database.compile_sqla_query(qry)
        if indent:
            sql = sqlparse.format(sql, reindent=True)
        return sql

    @classmethod
    def estimate_statement_cost(cls, statement: str, cursor: Any,) -> Dict[str, Any]:
        """
        Generate a SQL query that estimates the cost of a given statement.

        :param statement: A single SQL statement
        :param cursor: Cursor instance
        :return: Dictionary with different costs
        """
        raise Exception("Database does not support cost estimation")

    @classmethod
    def query_cost_formatter(cls, raw_cost: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Format cost estimate.

        :param raw_cost: Raw estimate from `estimate_query_cost`
        :return: Human readable cost estimate
        """
        raise Exception("Database does not support cost estimation")

    @classmethod
    def process_statement(cls, statement: str, database: "Database", user_name: str) -> str:
        """
        Process a SQL statement by stripping and mutating it.

        :param statement: A single SQL statement
        :param database: Database instance
        :param user_name: Effective username
        :return: Dictionary with different costs
        """

        parsed_query = ParsedQuery(statement)
        sql = parsed_query.stripped()
        sql_query_mutator = current_app.config["SQL_QUERY_MUTATOR"]
        if sql_query_mutator:
            sql = sql_query_mutator(sql, user_name, security_manager, database)

        return sql

    @classmethod
    def estimate_query_cost(
        cls, database: "Database", schema: str, sql: str, source: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        估计多语句SQL查询的成本。

        :param database: Database instance
        :param schema: Database schema
        :param sql: SQL query with possibly multiple statements
        :param source: Source of the query (eg, "sql_lab")
        """

        extra = database.get_extra() or {}
        if not cls.get_allow_cost_estimate(extra):
            raise Exception("Database does not support cost estimation")

        user_name = g.user.username if g.user and hasattr(g.user, "username") else None
        parsed_query = sql_parse.ParsedQuery(sql)
        statements = parsed_query.get_statements()

        engine = cls.get_engine(database, schema=schema, source=source)
        costs = []
        with closing(engine.raw_connection()) as conn:
            cursor = conn.cursor()
            for statement in statements:
                processed_statement = cls.process_statement(
                    statement, database, user_name
                )
                costs.append(cls.estimate_statement_cost(processed_statement, cursor))
        return costs

    @classmethod
    def modify_url_for_impersonation(
        cls, url: URL, impersonate_user: bool, username: Optional[str]
    ) -> None:
        """
        与用户一起修改SQL Alchemy URL对象以模拟（如果适用）。

        :param url: SQLAlchemy URL 对象
        :param impersonate_user: 指示是否启用模拟的标志
        :param username: 用户名称。
        """
        if impersonate_user and username is not None:
            url.username = username

    @classmethod
    def update_impersonation_config(
        cls, connect_args: Dict[str, Any], uri: str, username: Optional[str],
    ) -> None:
        """
        更新可以为模拟用户设置正确属性的配置字典

        :param connect_args: 要更新的配置。
        :param uri: 地址字符串。
        :param username: 用户名称。
        :return: None
        """

    @classmethod
    def execute(cls, cursor: Any, query: str, **kwargs: Any) -> None:
        """
        执行指定 SQL 查询。

        :param cursor: Cursor 实例。
        :param query: 要执行的查询字符串。
        :param kwargs: 要传递到 cursor.execute() 的参数。
        :return:
        """

        if not cls.allows_sql_comments:
            query = sql_parse.strip_comments_from_sql(query)

        if cls.arraysize:
            cursor.arraysize = cls.arraysize

        try:
            cursor.execute(query)
        except Exception as ex:
            raise cls.get_dbapi_mapped_exception(ex)

    @classmethod
    def make_label_compatible(cls, label: str) -> Union[str, quoted_name]:
        """
        Conditionally mutate and/or quote a sqlalchemy expression label. If
        force_column_alias_quotes is set to True, return the label as a
        sqlalchemy.sql.elements.quoted_name object to ensure that the select query
        and query results have same case. Otherwise return the mutated label as a
        regular string. If maxmimum supported column name length is exceeded,
        generate a truncated label by calling truncate_label().

        :param label: expected expression label/alias
        :return: conditionally mutated label supported by the db engine
        """
        label_mutated = cls._mutate_label(label)
        if (
            cls.max_column_name_length
            and len(label_mutated) > cls.max_column_name_length
        ):
            label_mutated = cls._truncate_label(label)
        if cls.force_column_alias_quotes:
            label_mutated = quoted_name(label_mutated, True)
        return label_mutated

    @classmethod
    def get_sqla_column_type(
        cls,
        column_type: Optional[str],
        column_type_mappings: Tuple[
            Tuple[
                Pattern[str],
                Union[TypeEngine, Callable[[Match[str]], TypeEngine]],
                GenericDataType,
            ],
            ...,
        ] = column_type_mappings,
    ) -> Union[Tuple[TypeEngine, GenericDataType], None]:
        """
        Return a sqlalchemy native column type that corresponds to the column type
        defined in the data source (return None to use default type inferred by
        SQLAlchemy). Override `column_type_mappings` for specific needs
        (see MSSQL for example of NCHAR/NVARCHAR handling).

        :param column_type: Column type returned by inspector
        :param column_type_mappings:
        :return: SqlAlchemy column type
        """

        if not column_type:
            return None

        for regex, sqla_type, generic_type in column_type_mappings:
            match = regex.match(column_type)
            if match:
                if callable(sqla_type):
                    return sqla_type(match), generic_type
                return sqla_type, generic_type
        return None

    @staticmethod
    def _mutate_label(label: str) -> str:
        """
        Most engines support mixed case aliases that can include numbers
        and special characters, like commas, parentheses etc. For engines that
        have restrictions on what types of aliases are supported, this method
        can be overridden to ensure that labels conform to the engine's
        limitations. Mutated labels should be deterministic (input label A always
        yields output label X) and unique (input labels A and B don't yield the same
        output label X).

        :param label: Preferred expression label
        :return: Conditionally mutated label
        """

        return label

    @classmethod
    def _truncate_label(cls, label: str) -> str:
        """
        In the case that a label exceeds the max length supported by the engine,
        this method is used to construct a deterministic and unique label based on
        the original label. By default this returns an md5 hash of the original label,
        conditionally truncated if the length of the hash exceeds the max column length
        of the engine.

        :param label: Expected expression label
        :return: Truncated label
        """
        label = md5_sha_from_str(label)
        # truncate hash if it exceeds max length
        if cls.max_column_name_length and len(label) > cls.max_column_name_length:
            label = label[: cls.max_column_name_length]
        return label

    @classmethod
    def column_datatype_to_string(cls, sqla_column_type: TypeEngine, dialect: Dialect) -> str:
        """
        Convert sqlalchemy column type to string representation.
        By default removes collation and character encoding info to avoid unnecessarily
        long datatypes.

        :param sqla_column_type: SqlAlchemy column type
        :param dialect: Sqlalchemy dialect
        :return: Compiled column type
        """

        sqla_column_type = sqla_column_type.copy()
        if hasattr(sqla_column_type, "collation"):
            sqla_column_type.collation = None
        if hasattr(sqla_column_type, "charset"):
            sqla_column_type.charset = None

        return sqla_column_type.compile(dialect=dialect).upper()

    @classmethod
    def get_function_names(cls, database: "Database") -> List[str]:
        """
        Get a list of function names that are able to be called on the database.
        Used for SQL Lab autocomplete.

        :param database: The database to get functions for
        :return: A list of function names useable in the database
        """
        return []

    @staticmethod
    def pyodbc_rows_to_tuples(data: List[Any]) -> List[Tuple[Any, ...]]:
        """
        Convert pyodbc.Row objects from `fetch_data` to tuples.

        :param data: List of tuples or pyodbc.Row objects
        :return: List of tuples
        """

        if data and type(data[0]).__name__ == "Row":
            data = [tuple(row) for row in data]

        return data

    @staticmethod
    def mutate_db_for_connection_test(database: "Database") -> None:
        """
        Some databases require passing additional parameters for validating database
        connections. This method makes it possible to mutate the database instance prior
        to testing if a connection is ok.

        :param database: instance to be mutated
        """
        return None

    @staticmethod
    def get_extra_params(database: "Database") -> Dict[str, Any]:
        """
        Some databases require adding elements to connection parameters,
        like passing certificates to `extra`. This can be done here.

        :param database: database instance from which to extract extras
        :raises CertificateException: If certificate is not valid/unparseable
        """

        extra: Dict[str, Any] = {}
        if database.extra:
            try:
                extra = json.loads(database.extra)
            except json.JSONDecodeError as ex:
                logger.error(ex, exc_info=True)
                raise ex
        return extra

    @classmethod
    def is_readonly_query(cls, parsed_query: ParsedQuery) -> bool:
        """Pessimistic readonly, 100% sure statement won't mutate anything"""
        return (
            parsed_query.is_select()
            or parsed_query.is_explain()
            or parsed_query.is_show()
        )

    @classmethod
    def is_select_query(cls, parsed_query: ParsedQuery) -> bool:
        """
        Determine if the statement should be considered as SELECT statement.
        Some query dialects do not contain "SELECT" word in queries (eg. Kusto)
        """
        return parsed_query.is_select()

    @classmethod
    @memoized
    def get_column_spec(
        cls,
        native_type: Optional[str],
        source: utils.ColumnTypeSource = utils.ColumnTypeSource.GET_TABLE,
        column_type_mappings: Tuple[
            Tuple[
                Pattern[str],
                Union[TypeEngine, Callable[[Match[str]], TypeEngine]],
                GenericDataType,
            ],
            ...,
        ] = column_type_mappings,
    ) -> Union[ColumnSpec, None]:
        """
        将数据库类型转换为sqlalchemy列类型。

        :param native_type: 原生数据库类型
        :param source: 来自数据库表或游标说明的类型
        :param column_type_mappings:
        :return: ColumnSpec object
        """

        col_types = cls.get_sqla_column_type(
            native_type, column_type_mappings=column_type_mappings
        )
        if col_types:
            column_type, generic_type = col_types
            # wrap temporal types in custom type that supports literal binding
            # using datetimes
            if generic_type == GenericDataType.TEMPORAL:
                column_type = literal_dttm_type_factory(
                    type(column_type), cls, native_type or ""
                )
            is_dttm = generic_type == GenericDataType.TEMPORAL
            return ColumnSpec(
                sqla_type=column_type, generic_type=generic_type, is_dttm=is_dttm
            )
        return None

    @classmethod
    def has_implicit_cancel(cls) -> bool:
        """
        如果活动游标处理查询的隐式取消，则返回True，否则返回False。

        :return: 活动游标是否隐式取消查询
        :see: handle_cursor
        """

        return False

    @classmethod
    def get_cancel_query_id(cls, cursor: Any, query: Query) -> Optional[str]:
        """
        从数据库引擎中选择唯一标识要取消的查询的标识符。标识符通常是会话id、进程id或类似的。

        :param cursor: 将在其中执行查询的游标实例
        :param query: 查询实例。
        :return: 查询标识。
        """

        return None

    @classmethod
    def cancel_query(cls, cursor: Any, query: Query, cancel_query_id: str) -> bool:
        """
        取消基础数据库中的查询。

        :param cursor: 将新游标实例添加到查询的数据库
        :param query: 查询实例
        :param cancel_query_id: 由 get_cancel_query_payload 返回的值或查询对象的其它方法设置的。
        :return: 如果查询成功取消，则为True，否则为False
        """

        return False


class BasicParametersSchema(Schema):
    """数据库连接参数结构，代替 SQLAlchemy URI。

    定义字段及其类型和约束：

    - username：用户名称，必须的，允许None。
    - password：用户密码，允许None。
    - host：主机名称或IP地址，必须的。
    - port：端口号，必须的。
    - database：数据库名称，必须的。
    - query：查询参数，字典。
    - encryption：是否加密。
    """

    username = fields.String(required=True, allow_none=True, description=__("Username"))
    password = fields.String(allow_none=True, description=__("Password"))
    host = fields.String(required=True, description=__("Hostname or IP address"))
    port = fields.Integer(
        required=True,
        description=__("Database port"),
        validate=Range(min=0, max=2 ** 16, max_inclusive=False),
    )
    database = fields.String(required=True, description=__("Database name"))
    query = fields.Dict(
        keys=fields.Str(), values=fields.Raw(), description=__("Additional parameters")
    )
    encryption = fields.Boolean(
        required=False, description=__("Use an encrypted connection to the database")
    )


class BasicParametersType(TypedDict, total=False):
    """数据库基本参数类型，定义数据库连接中每个参数及其类型。
    username、password、host、port、database、query、encryption。
    """

    username: Optional[str]
    password: Optional[str]
    host: str
    port: int
    database: str
    query: Dict[str, Any]
    encryption: bool


class BasicParametersMixin:
    """
    用于通过字典配置DB引擎规范的Mixin。

    有了这个mixin，可以通过单个参数来配置SQLAlchemy引擎，而不是通过完整的SQLAlchemy URI。
    此mixin用于最常见的URI模式：

        engine+driver://user:password@host:port/dbname[?key=value&key=value...]

    """

    # schema describing the parameters used to configure the DB
    parameters_schema = BasicParametersSchema()
    """描述用于配置数据库的参数的架构."""
    # recommended driver name for the DB engine spec
    default_driver = ""
    """DB引擎规范的推荐驱动程序名称"""
    # placeholder with the SQLAlchemy URI template
    sqlalchemy_uri_placeholder = (
        "engine+driver://user:password@host:port/dbname[?key=value&key=value...]"
    )
    """带有SQLAlchemy URI模板的占位符"""
    # query parameter to enable encryption in the database connection for Postgres
    # this would be `{"sslmode": "verify-ca"}`, eg.
    encryption_parameters: Dict[str, str] = {}
    """用于在Postgres的数据库连接中启用加密的查询参数，这将是 `{"sslmode": "verify-ca"}`。"""

    @classmethod
    def build_sqlalchemy_uri(
        cls,
        parameters: BasicParametersType,
        encryted_extra: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        构建 SQLAlchemy URI 地址。

        :param parameters:
        :param encryted_extra:
        :return:
        """

        # make a copy so that we don't update the original
        query = parameters.get("query", {}).copy()
        if parameters.get("encryption"):
            if not cls.encryption_parameters:
                raise Exception("Unable to build a URL with encryption enabled")
            query.update(cls.encryption_parameters)

        return str(
            URL(
                f"{cls.engine}+{cls.default_driver}".rstrip("+"),  # type: ignore
                username=parameters.get("username"),
                password=parameters.get("password"),
                host=parameters["host"],
                port=parameters["port"],
                database=parameters["database"],
                query=query,
            )
        )

    @classmethod
    def get_parameters_from_uri(
        cls, uri: str, encrypted_extra: Optional[Dict[str, Any]] = None
    ) -> BasicParametersType:
        """
        从指定 SQLAlchemy URI 字符串获取参数对象。

        :param uri:
        :param encrypted_extra:
        :return:
        """

        url = make_url(uri)
        query = {
            key: value
            for (key, value) in url.query.items()
            if (key, value) not in cls.encryption_parameters.items()
        }
        encryption = all(
            item in url.query.items() for item in cls.encryption_parameters.items()
        )
        return {
            "username": url.username,
            "password": url.password,
            "host": url.host,
            "port": url.port,
            "database": url.database,
            "query": query,
            "encryption": encryption,
        }

    @classmethod
    def validate_parameters(
        cls, parameters: BasicParametersType
    ) -> List[RabbitaiError]:
        """
        Validates any number of parameters, for progressive validation.

        If only the hostname is present it will check if the name is resolvable. As more
        parameters are present in the request, more validation is done.
        """

        errors: List[RabbitaiError] = []

        required = {"host", "port", "username", "database"}
        present = {key for key in parameters if parameters.get(key, ())}
        missing = sorted(required - present)

        if missing:
            errors.append(
                RabbitaiError(
                    message=f'One or more parameters are missing: {", ".join(missing)}',
                    error_type=RabbitaiErrorType.CONNECTION_MISSING_PARAMETERS_ERROR,
                    level=ErrorLevel.WARNING,
                    extra={"missing": missing},
                ),
            )

        host = parameters.get("host", None)
        if not host:
            return errors
        if not is_hostname_valid(host):
            errors.append(
                RabbitaiError(
                    message="The hostname provided can't be resolved.",
                    error_type=RabbitaiErrorType.CONNECTION_INVALID_HOSTNAME_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["host"]},
                ),
            )
            return errors

        port = parameters.get("port", None)
        if not port:
            return errors
        try:
            port = int(port)
        except (ValueError, TypeError):
            errors.append(
                RabbitaiError(
                    message="Port must be a valid integer.",
                    error_type=RabbitaiErrorType.CONNECTION_INVALID_PORT_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )
        if not (isinstance(port, int) and 0 <= port < 2 ** 16):
            errors.append(
                RabbitaiError(
                    message=(
                        "The port must be an integer between 0 and 65535 "
                        "(inclusive)."
                    ),
                    error_type=RabbitaiErrorType.CONNECTION_INVALID_PORT_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )
        elif not is_port_open(host, port):
            errors.append(
                RabbitaiError(
                    message="The port is closed.",
                    error_type=RabbitaiErrorType.CONNECTION_PORT_CLOSED_ERROR,
                    level=ErrorLevel.ERROR,
                    extra={"invalid": ["port"]},
                ),
            )

        return errors

    @classmethod
    def parameters_json_schema(cls) -> Any:
        """
        以 OpenAPI 的形式返回配置参数。
        """
        if not cls.parameters_schema:
            return None

        spec = APISpec(
            title="数据库参数",
            version="1.0.0",
            openapi_version="3.0.2",
            plugins=[MarshmallowPlugin()],
        )
        spec.components.schema(cls.__name__, schema=cls.parameters_schema)
        return spec.to_dict()["components"]["schemas"][cls.__name__]
