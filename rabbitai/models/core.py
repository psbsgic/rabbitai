# -*- coding: utf-8 -*-

"""A collection of ORM sqlalchemy models for RabbitAI"""

import enum
import json
import logging
import textwrap
from ast import literal_eval
from contextlib import closing
from copy import deepcopy
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type

import numpy
import pandas as pd
import sqlalchemy as sqla
import sqlparse
from flask import g, request
from flask_appbuilder import Model
from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.engine import Dialect, Engine, url
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.engine.url import make_url, URL
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import expression, Select

from rabbitai import app, db_engine_specs, is_feature_enabled
from rabbitai.db_engine_specs.base import TimeGrain
from rabbitai.extensions import cache_manager, encrypted_field_factory, security_manager
from rabbitai.models.helpers import AuditMixinNullable, ImportExportMixin
from rabbitai.models.tags import FavStarUpdater
from rabbitai.result_set import RabbitaiResultSet
from rabbitai.utils import cache as cache_util, core as utils
from rabbitai.utils.memoized import memoized

config = app.config
custom_password_store = config["SQLALCHEMY_CUSTOM_PASSWORD_STORE"]
stats_logger = config["STATS_LOGGER"]
log_query = config["QUERY_LOGGER"]
metadata = Model.metadata

logger = logging.getLogger(__name__)

PASSWORD_MASK = "X" * 10
DB_CONNECTION_MUTATOR = config["DB_CONNECTION_MUTATOR"]


class Url(Model, AuditMixinNullable):
    """网络地址对象关系模型。"""

    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    url = Column(Text)


class KeyValue(Model):
    """key-value 对对象关系模型。"""

    __tablename__ = "keyvalue"
    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False)


class CssTemplate(Model, AuditMixinNullable):
    """CSS 模板对象关系模型，存储仪表盘的CSS模板。"""

    __tablename__ = "css_templates"
    id = Column(Integer, primary_key=True)
    template_name = Column(String(250))
    css = Column(Text, default="")


class ConfigurationMethod(str, enum.Enum):
    """配置方法枚举，SQLALCHEMY_FORM、DYNAMIC_FORM。"""

    SQLALCHEMY_FORM = "sqlalchemy_form"
    DYNAMIC_FORM = "dynamic_form"


class Database(Model, AuditMixinNullable, ImportExportMixin):
    """数据库对象关系模型，存储访问特定数据库相关信息和选项，提供获取数据库对象及其元数据的方法。"""

    __tablename__ = "dbs"
    type = "table"
    """类型，默认：table"""
    __table_args__ = (UniqueConstraint("database_name"),)

    # region Column

    id = Column(Integer, primary_key=True)
    """唯一标识"""
    verbose_name = Column(String(250), unique=True)
    """显示名称"""
    database_name = Column(String(250), unique=True, nullable=False)
    """数据库名称，唯一、用于权限"""
    sqlalchemy_uri = Column(String(1024), nullable=False)
    """数据库 sqlalchemy 地址"""
    password = Column(encrypted_field_factory.create(String(1024)))
    """密码"""
    cache_timeout = Column(Integer)
    """超时"""
    select_as_create_table_as = Column(Boolean, default=False)
    """是否使用SELECT作为创建数据表"""
    expose_in_sqllab = Column(Boolean, default=True)
    """是否在SQL工具中公开"""
    configuration_method = Column(
        String(255), server_default=ConfigurationMethod.SQLALCHEMY_FORM.value
    )
    """配置方法"""
    allow_run_async = Column(Boolean, default=False)
    """是否允许异步运行"""
    allow_csv_upload = Column(Boolean, default=False)
    """是否允许上传CSV"""
    allow_ctas = Column(Boolean, default=False)
    """是否允许创建数据表作为SELECT语句"""
    allow_cvas = Column(Boolean, default=False)
    """是否允许创建视图作为SELECT语句"""
    allow_dml = Column(Boolean, default=False)
    """是否允许DML"""
    force_ctas_schema = Column(String(250))
    """强制创建数据表作为SELECT语句模式"""
    allow_multi_schema_metadata_fetch = Column(Boolean, default=False)
    """是否允许多模式元数据提取"""
    extra = Column(
        Text,
        default=textwrap.dedent(
            """\
    {
        "metadata_params": {},
        "engine_params": {},
        "metadata_cache_timeout": {},
        "schemas_allowed_for_csv_upload": []
    }
    """
        ),
    )
    """额外信息"""
    encrypted_extra = Column(encrypted_field_factory.create(Text), nullable=True)
    """加密的额外信息"""
    impersonate_user = Column(Boolean, default=False)
    """是否模拟用户"""
    server_cert = Column(encrypted_field_factory.create(Text), nullable=True)
    """服务器证书"""

    # endregion

    export_fields = [
        "database_name",
        "sqlalchemy_uri",
        "cache_timeout",
        "expose_in_sqllab",
        "allow_run_async",
        "allow_ctas",
        "allow_cvas",
        "allow_csv_upload",
        "extra",
    ]
    """导出字段名称的列表"""
    extra_import_fields = ["password"]
    """额外导入字段名称的列表。"""
    export_children = ["tables"]
    """导出的子对象类名称的列表。"""

    def __repr__(self) -> str:
        """返回数据库的名称"""
        return self.name

    # region Properties

    @property
    def name(self) -> str:
        """获取数据库对象名称，verbose_name或database_name"""

        return self.verbose_name if self.verbose_name else self.database_name

    @property
    def allows_subquery(self) -> bool:
        """是否允许子查询，数据库引擎规范。"""
        return self.db_engine_spec.allows_subqueries

    @property
    def function_names(self) -> List[str]:
        """返回数据库支持的函数名称列表，数据库引擎规范。"""

        try:
            return self.db_engine_spec.get_function_names(self)
        except Exception as ex:  # pylint: disable=broad-except
            # function_names property is used in bulk APIs and should not hard crash
            # more info in: https://github.com/apache/rabbitai/issues/9678
            logger.error(
                "Failed to fetch database function names with error: %s",
                str(ex),
                exc_info=True,
            )
        return []

    @property
    def allows_cost_estimate(self) -> bool:
        """是否允许耗时评估，基于：extra和数据库引擎规范。"""
        extra = self.get_extra() or {}
        cost_estimate_enabled: bool = extra.get("cost_estimate_enabled")  # type: ignore

        return (
            self.db_engine_spec.get_allow_cost_estimate(extra) and cost_estimate_enabled
        )

    @property
    def allows_virtual_table_explore(self) -> bool:
        """是否允许虚拟数据表探索，基于：extra。"""
        extra = self.get_extra()

        return bool(extra.get("allows_virtual_table_explore", True))

    @property
    def explore_database_id(self) -> int:
        """获取数据库浏览标识，基于：extra。"""
        return self.get_extra().get("explore_database_id", self.id)

    @property
    def data(self) -> Dict[str, Any]:
        """获取要发送到客户端数据，Json字典。"""
        return {
            "id": self.id,
            "name": self.database_name,
            "backend": self.backend,
            "configuration_method": self.configuration_method,
            "allow_multi_schema_metadata_fetch": self.allow_multi_schema_metadata_fetch,
            "allows_subquery": self.allows_subquery,
            "allows_cost_estimate": self.allows_cost_estimate,
            "allows_virtual_table_explore": self.allows_virtual_table_explore,
            "explore_database_id": self.explore_database_id,
            "parameters": self.parameters,
        }

    @property
    def unique_name(self) -> str:
        """获取数据库的唯一名称。"""
        return self.database_name

    @property
    def url_object(self) -> URL:
        """获取数据库访问地址对象 URL。"""
        return make_url(self.sqlalchemy_uri_decrypted)

    @property
    def backend(self) -> str:
        """从 sqlalchemy uri，获取数据库后端。"""
        sqlalchemy_url = make_url(self.sqlalchemy_uri_decrypted)

        return sqlalchemy_url.get_backend_name()

    @property
    def parameters(self) -> Dict[str, Any]:
        """从 sqlalchemy uri，获取数据库连接参数。"""

        uri = make_url(self.sqlalchemy_uri_decrypted)
        encrypted_extra = self.get_encrypted_extra()
        try:
            parameters = self.db_engine_spec.get_parameters_from_uri(uri, encrypted_extra=encrypted_extra)
        except Exception:
            parameters = {}

        return parameters

    @property
    def metadata_cache_timeout(self) -> Dict[str, Any]:
        """获取元数据缓存超时（字典），基于：extra。"""
        return self.get_extra().get("metadata_cache_timeout", {})

    @property
    def schema_cache_enabled(self) -> bool:
        return "schema_cache_timeout" in self.metadata_cache_timeout

    @property
    def schema_cache_timeout(self) -> Optional[int]:
        return self.metadata_cache_timeout.get("schema_cache_timeout")

    @property
    def table_cache_enabled(self) -> bool:
        return "table_cache_timeout" in self.metadata_cache_timeout

    @property
    def table_cache_timeout(self) -> Optional[int]:
        return self.metadata_cache_timeout.get("table_cache_timeout")

    @property
    def default_schemas(self) -> List[str]:
        """获取默认模式，基于：extra。"""
        return self.get_extra().get("default_schemas", [])

    @property
    def connect_args(self) -> Dict[str, Any]:
        """获取连接参数，基于：extra。"""
        return self.get_extra().get("engine_params", {}).get("connect_args", {})

    # endregion

    @classmethod
    def get_password_masked_url_from_uri(cls, uri: str) -> URL:
        """
        依据指定地址构建密码掩码地址。

        :param uri:
        :return:
        """
        sqlalchemy_url = make_url(uri)
        return cls.get_password_masked_url(sqlalchemy_url)

    @classmethod
    def get_password_masked_url(cls, masked_url: URL) -> URL:
        """
        获取密码掩码地址，即将密码设置为：XXXXXXXXXX。

        :param masked_url: 掩码地址。
        :return:
        """
        url_copy = deepcopy(masked_url)
        if url_copy.password is not None:
            url_copy.password = PASSWORD_MASK
        return url_copy

    def set_sqlalchemy_uri(self, uri: str) -> None:
        """
        设置指定地址字符串为数据库连接字符串。

        :param uri:
        :return:
        """
        conn = sqla.engine.url.make_url(uri.strip())
        if conn.password != PASSWORD_MASK and not custom_password_store:
            # do not over-write the password with the password mask
            self.password = conn.password
        conn.password = PASSWORD_MASK if conn.password else None
        self.sqlalchemy_uri = str(conn)  # hides the password

    def get_effective_user(self, object_url: URL, user_name: Optional[str] = None,) -> Optional[str]:
        """
        Get the effective user, especially during impersonation.

        :param object_url: SQL Alchemy URL object
        :param user_name: Default username
        :return: The effective username
        """

        effective_username = None
        if self.impersonate_user:
            effective_username = object_url.username
            if user_name:
                effective_username = user_name
            elif (
                hasattr(g, "user")
                and hasattr(g.user, "username")
                and g.user.username is not None
            ):
                effective_username = g.user.username
        return effective_username

    @memoized(watch=("impersonate_user", "sqlalchemy_uri_decrypted", "extra"))
    def get_sqla_engine(
        self,
        schema: Optional[str] = None,
        nullpool: bool = True,
        user_name: Optional[str] = None,
        source: Optional[utils.QuerySource] = None,
    ) -> Engine:
        """
        依据该数据库对象提供的额外信息和方法，以及指定参数调用 create_engine 返回数据库引擎。

        :param schema: 模式。
        :param nullpool: 是否无连接池。
        :param user_name: 用户名称。
        :param source: 查询源。
        :return: 数据库引擎。
        """

        extra = self.get_extra()
        sqlalchemy_url = make_url(self.sqlalchemy_uri_decrypted)
        self.db_engine_spec.adjust_database_uri(sqlalchemy_url, schema)
        effective_username = self.get_effective_user(sqlalchemy_url, user_name)
        # If using MySQL or Presto for example, will set url.username
        # If using Hive, will not do anything yet since that relies on a
        # configuration parameter instead.
        self.db_engine_spec.modify_url_for_impersonation(
            sqlalchemy_url, self.impersonate_user, effective_username
        )

        masked_url = self.get_password_masked_url(sqlalchemy_url)
        logger.debug("Database.get_sqla_engine(). Masked URL: %s", str(masked_url))

        params = extra.get("engine_params", {})
        if nullpool:
            params["poolclass"] = NullPool

        connect_args = params.get("connect_args", {})
        if self.impersonate_user:
            self.db_engine_spec.update_impersonation_config(
                connect_args, str(sqlalchemy_url), effective_username
            )

        if connect_args:
            params["connect_args"] = connect_args

        params.update(self.get_encrypted_extra())

        if DB_CONNECTION_MUTATOR:
            if not source and request and request.referrer:
                if "/rabbitai/dashboard/" in request.referrer:
                    source = utils.QuerySource.DASHBOARD
                elif "/rabbitai/explore/" in request.referrer:
                    source = utils.QuerySource.CHART
                elif "/rabbitai/sqllab/" in request.referrer:
                    source = utils.QuerySource.SQL_LAB

            sqlalchemy_url, params = DB_CONNECTION_MUTATOR(
                sqlalchemy_url, params, effective_username, security_manager, source
            )

        return create_engine(sqlalchemy_url, **params)

    def get_reserved_words(self) -> Set[str]:
        """获取该数据库支持的保留关键字集合"""
        return self.get_dialect().preparer.reserved_words

    def get_quoter(self) -> Callable[[str, Any], str]:
        """获取该数据库支持的定界方法。"""
        return self.get_dialect().identifier_preparer.quote

    def get_df(
        self,
        sql: str,
        schema: Optional[str] = None,
        mutator: Optional[Callable[[pd.DataFrame], None]] = None,
    ) -> pd.DataFrame:
        """
        返回数据帧pd.DataFrame。

        :param sql: SQL查询字符串。
        :param schema: 模式。
        :param mutator: 修改器，用于更改数据帧。
        :return:
        """

        sqls = [str(s).strip(" ;") for s in sqlparse.parse(sql)]

        engine = self.get_sqla_engine(schema=schema)
        username = utils.get_username()

        def needs_conversion(df_series: pd.Series) -> bool:
            return (
                not df_series.empty
                and isinstance(df_series, pd.Series)
                and isinstance(df_series[0], (list, dict))
            )

        def _log_query(sql: str) -> None:
            if log_query:
                log_query(engine.url, sql, schema, username, __name__, security_manager)

        with closing(engine.raw_connection()) as conn:
            cursor = conn.cursor()
            for sql_ in sqls[:-1]:
                _log_query(sql_)
                self.db_engine_spec.execute(cursor, sql_)
                cursor.fetchall()

            _log_query(sqls[-1])
            self.db_engine_spec.execute(cursor, sqls[-1])

            data = self.db_engine_spec.fetch_data(cursor)
            result_set = RabbitaiResultSet(
                data, cursor.description, self.db_engine_spec
            )
            df = result_set.to_pandas_df()
            if mutator:
                df = mutator(df)

            for col, coltype in df.dtypes.to_dict().items():
                if coltype == numpy.object_ and needs_conversion(df[col]):
                    df[col] = df[col].apply(utils.json_dumps_w_dates)

            return df

    def compile_sqla_query(self, qry: Select, schema: Optional[str] = None) -> str:
        """
        编译SQLA查询。

        :param qry: SELECT查询语句。
        :param schema: 模式。
        :return:
        """

        engine = self.get_sqla_engine(schema=schema)

        sql = str(qry.compile(engine, compile_kwargs={"literal_binds": True}))

        if (engine.dialect.identifier_preparer._double_percents):
            sql = sql.replace("%%", "%")

        return sql

    def select_star(
        self,
        table_name: str,
        schema: Optional[str] = None,
        limit: int = 100,
        show_cols: bool = False,
        indent: bool = True,
        latest_partition: bool = False,
        cols: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        基于该数据库的方言，生成 ``select *`` 语句。

        :param table_name: 数据表名称。
        :param schema: 模式名称。
        :param limit: 限制。
        :param show_cols: 是否显示列。
        :param indent: 是否缩进。
        :param latest_partition: 是否最近分区。
        :param cols: 列信息的列表。
        :return:
        """

        eng = self.get_sqla_engine(schema=schema, source=utils.QuerySource.SQL_LAB)
        return self.db_engine_spec.select_star(
            self,
            table_name,
            schema=schema,
            engine=eng,
            limit=limit,
            show_cols=show_cols,
            indent=indent,
            latest_partition=latest_partition,
            cols=cols,
        )

    def apply_limit_to_sql(self, sql: str, limit: int = 1000, force: bool = False) -> str:
        """
        应用限制到SQL语句中。

        :param sql: SQL语句。
        :param limit: 限制。
        :param force: 是否强制。
        :return:
        """
        return self.db_engine_spec.apply_limit_to_sql(sql, limit, self, force=force)

    def safe_sqlalchemy_uri(self) -> str:
        """获取数据库连接地址字符串。"""
        return self.sqlalchemy_uri

    @property
    def inspector(self) -> Inspector:
        """获取该数据库的探测器。"""

        engine = self.get_sqla_engine()
        return sqla.inspect(engine)

    @cache_util.memoized_func(
        key=lambda self, *args, **kwargs: f"db:{self.id}:schema:None:table_list",
        cache=cache_manager.data_cache,
    )
    def get_all_table_names_in_database(
        self,
        cache: bool = False,
        cache_timeout: Optional[bool] = None,
        force: bool = False,
    ) -> List[utils.DatasourceName]:
        """
        获取数据库中的所有数据表名称。

        :param cache:
        :param cache_timeout:
        :param force:
        :return:
        """

        if not self.allow_multi_schema_metadata_fetch:
            return []

        return self.db_engine_spec.get_all_datasource_names(self, "table")

    @cache_util.memoized_func(
        key=lambda self, *args, **kwargs: f"db:{self.id}:schema:None:view_list",
        cache=cache_manager.data_cache,
    )
    def get_all_view_names_in_database(
        self,
        cache: bool = False,
        cache_timeout: Optional[bool] = None,
        force: bool = False,
    ) -> List[utils.DatasourceName]:
        """
        获取数据库中所有视图名称。

        :param cache:
        :param cache_timeout:
        :param force:
        :return:
        """
        if not self.allow_multi_schema_metadata_fetch:
            return []
        return self.db_engine_spec.get_all_datasource_names(self, "view")

    @cache_util.memoized_func(
        key=lambda self, schema, *args, **kwargs: f"db:{self.id}:schema:{schema}:table_list",  # type: ignore
        cache=cache_manager.data_cache,
    )
    def get_all_table_names_in_schema(
        self,
        schema: str,
        cache: bool = False,
        cache_timeout: Optional[int] = None,
        force: bool = False,
    ) -> List[utils.DatasourceName]:
        """获取模式中所有数据表名称。

        For unused parameters, they are referenced in
        cache_util.memoized_func decorator.

        :param schema: schema name
        :param cache: whether cache is enabled for the function
        :param cache_timeout: timeout in seconds for the cache
        :param force: whether to force refresh the cache
        :return: list of tables
        """
        try:
            tables = self.db_engine_spec.get_table_names(
                database=self, inspector=self.inspector, schema=schema
            )
            return [
                utils.DatasourceName(table=table, schema=schema) for table in tables
            ]
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning(ex)

    @cache_util.memoized_func(
        key=lambda self, schema, *args, **kwargs: f"db:{self.id}:schema:{schema}:view_list",  # type: ignore
        cache=cache_manager.data_cache,
    )
    def get_all_view_names_in_schema(
        self,
        schema: str,
        cache: bool = False,
        cache_timeout: Optional[int] = None,
        force: bool = False,
    ) -> List[utils.DatasourceName]:
        """获取模式中所有视图名称。

        For unused parameters, they are referenced in
        cache_util.memoized_func decorator.

        :param schema: schema name
        :param cache: whether cache is enabled for the function
        :param cache_timeout: timeout in seconds for the cache
        :param force: whether to force refresh the cache
        :return: list of views
        """
        try:
            views = self.db_engine_spec.get_view_names(
                database=self, inspector=self.inspector, schema=schema
            )
            return [utils.DatasourceName(table=view, schema=schema) for view in views]
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning(ex)

    @cache_util.memoized_func(
        key=lambda self, *args, **kwargs: f"db:{self.id}:schema_list",
        cache=cache_manager.data_cache,
    )
    def get_all_schema_names(
        self,
        cache: bool = False,
        cache_timeout: Optional[int] = None,
        force: bool = False,
    ) -> List[str]:
        """获取所有模式名称。

        For unused parameters, they are referenced in
        cache_util.memoized_func decorator.

        :param cache: whether cache is enabled for the function
        :param cache_timeout: timeout in seconds for the cache
        :param force: whether to force refresh the cache
        :return: schema list
        """
        return self.db_engine_spec.get_schema_names(self.inspector)

    @property
    def db_engine_spec(self) -> Type[db_engine_specs.BaseEngineSpec]:
        """获取数据库引擎规范。"""
        return self.get_db_engine_spec_for_backend(self.backend)

    @classmethod
    @memoized
    def get_db_engine_spec_for_backend(cls, backend: str) -> Type[db_engine_specs.BaseEngineSpec]:
        """
        获取指定后台的数据库引擎规范。

        :param backend: 后台。
        :return:
        """

        engines = db_engine_specs.get_engine_specs()
        return engines.get(backend, db_engine_specs.BaseEngineSpec)

    def grains(self) -> Tuple[TimeGrain, ...]:
        """基于数据库规范，获取数据库特定时间粒度表达式。

        The idea here is to make it easy for users to change the time grain
        from a datetime (maybe the source grain is arbitrary timestamps, daily
        or 5 minutes increments) to another, "truncated" datetime. Since
        each database has slightly different but similar datetime functions,
        this allows a mapping between database engines and actual functions.
        """
        return self.db_engine_spec.get_time_grains()

    def get_extra(self) -> Dict[str, Any]:
        """
        返回数据库引擎的额外参数字典，这些额外信息是由数据库规范定义的额外参数。

        :return: 额外数据字典。
        """
        return self.db_engine_spec.get_extra_params(self)

    def get_encrypted_extra(self) -> Dict[str, Any]:
        """
        获取加密的额外参数，即：encrypted_extra 属性值的Json形式。

        :return:
        """

        encrypted_extra = {}
        if self.encrypted_extra:
            try:
                encrypted_extra = json.loads(self.encrypted_extra)
            except json.JSONDecodeError as ex:
                logger.error(ex, exc_info=True)
                raise ex
        return encrypted_extra

    def get_table(self, table_name: str, schema: Optional[str] = None) -> Table:
        """
        获取数据表对象关系模型 Table。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return: 数据表对象模型 Table。
        """

        extra = self.get_extra()
        meta = MetaData(**extra.get("metadata_params", {}))
        return Table(
            table_name,
            meta,
            schema=schema or None,
            autoload=True,
            autoload_with=self.get_sqla_engine(),
        )

    def get_table_comment(self, table_name: str, schema: Optional[str] = None) -> Optional[str]:
        """
        基于数据库规范，获取指定数据表的注释。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return:
        """
        return self.db_engine_spec.get_table_comment(self.inspector, table_name, schema)

    def get_columns(self, table_name: str, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        基于数据库规范，获取指定数据表的列名称及其对象的字典。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return:
        """
        return self.db_engine_spec.get_columns(self.inspector, table_name, schema)

    def get_indexes(self, table_name: str, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        基于数据库规范，获取指定数据表的索引字典。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return:
        """
        indexes = self.inspector.get_indexes(table_name, schema)
        return self.db_engine_spec.normalize_indexes(indexes)

    def get_pk_constraint(self, table_name: str, schema: Optional[str] = None) -> Dict[str, Any]:
        """
        基于探测器，获取指定数据表的主键约束字典。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return:
        """

        pk_constraint = self.inspector.get_pk_constraint(table_name, schema) or {}
        return {
            key: utils.base_json_conv(value) for key, value in pk_constraint.items()
        }

    def get_foreign_keys(self, table_name: str, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        基于探测器，获取指定数据表的外键。

        :param table_name: 数据表名称。
        :param schema: 模式。
        :return:
        """
        return self.inspector.get_foreign_keys(table_name, schema)

    def get_schema_access_for_csv_upload(self,) -> List[str]:
        """获取CVS上传的模式访问。"""
        allowed_databases = self.get_extra().get("schemas_allowed_for_csv_upload", [])

        if isinstance(allowed_databases, str):
            allowed_databases = literal_eval(allowed_databases)

        if hasattr(g, "user"):
            extra_allowed_databases = config["ALLOWED_USER_CSV_SCHEMA_FUNC"](
                self, g.user
            )
            allowed_databases += extra_allowed_databases
        return sorted(set(allowed_databases))

    @property
    def sqlalchemy_uri_decrypted(self) -> str:
        """获取解密的数据库连接地址。"""

        try:
            conn = sqla.engine.url.make_url(self.sqlalchemy_uri)
        except (ArgumentError, ValueError):
            # if the URI is invalid, ignore and return a placeholder url
            # (so users see 500 less often)
            return "dialect://invalid_uri"
        if custom_password_store:
            conn.password = custom_password_store(conn)
        else:
            conn.password = self.password
        return str(conn)

    @property
    def sql_url(self) -> str:
        """获取SQL访问地址。"""
        return f"/rabbitai/sql/{self.id}/"

    @hybrid_property
    def perm(self) -> str:
        """获取权限。"""
        return f"[{self.database_name}].(id:{self.id})"

    @perm.expression
    def perm(cls) -> str:
        """返回权限。"""

        return (
            "[" + cls.database_name + "].(id:" + expression.cast(cls.id, String) + ")"
        )

    def get_perm(self) -> str:
        """获取权限。"""
        return self.perm

    def has_table(self, table: Table) -> bool:
        """
        是否有指定数据表。

        :param table: 数据表模型。
        :return:
        """
        engine = self.get_sqla_engine()
        return engine.has_table(table.table_name, table.schema or None)

    def has_table_by_name(self, table_name: str, schema: Optional[str] = None) -> bool:
        """
        是否有指定数据表名称的数据表。

        :param table_name:
        :param schema:
        :return:
        """
        engine = self.get_sqla_engine()
        return engine.has_table(table_name, schema)

    @memoized
    def get_dialect(self) -> Dialect:
        """依据 sqlalchemy_uri 获取数据库方言。"""

        sqla_url = url.make_url(self.sqlalchemy_uri_decrypted)
        return sqla_url.get_dialect()()


sqla.event.listen(Database, "after_insert", security_manager.set_perm)
sqla.event.listen(Database, "after_update", security_manager.set_perm)


class Log(Model):
    """用于将 RabbitAI 操作记录到数据库的ORM对象"""

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(512))
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    dashboard_id = Column(Integer)
    slice_id = Column(Integer)
    json = Column(Text)
    user = relationship(
        security_manager.user_model, backref="logs", foreign_keys=[user_id]
    )
    dttm = Column(DateTime, default=datetime.utcnow)
    duration_ms = Column(Integer)
    referrer = Column(String(1024))


class FavStarClassName(str, enum.Enum):
    """评价对象类名称枚举，CHART、DASHBOARD。"""

    CHART = "slice"
    DASHBOARD = "Dashboard"


class FavStar(Model):
    """评价星级对象关系模型。"""

    __tablename__ = "favstar"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    class_name = Column(String(50))
    obj_id = Column(Integer)
    dttm = Column(DateTime, default=datetime.utcnow)


# events for updating tags
if is_feature_enabled("TAGGING_SYSTEM"):
    sqla.event.listen(FavStar, "after_insert", FavStarUpdater.after_insert)
    sqla.event.listen(FavStar, "after_delete", FavStarUpdater.after_delete)
