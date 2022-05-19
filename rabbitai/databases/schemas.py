# -*- coding: utf-8 -*-

import inspect
import json
from typing import Any, Dict, Optional, Type

from flask import current_app
from flask_babel import lazy_gettext as _
from marshmallow import EXCLUDE, fields, pre_load, Schema, validates_schema
from marshmallow.validate import Length, ValidationError
from marshmallow_enum import EnumField
from sqlalchemy import MetaData
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError

from rabbitai.db_engine_specs import BaseEngineSpec, get_engine_specs
from rabbitai.exceptions import CertificateException, RabbitaiSecurityException
from rabbitai.models.core import ConfigurationMethod, PASSWORD_MASK
from rabbitai.security.analytics_db_safety import check_sqlalchemy_uri
from rabbitai.utils.core import markdown, parse_ssl_cert

database_schemas_query_schema = {
    "type": "object",
    "properties": {"force": {"type": "boolean"}},
}
"""数据库模式查询结构。"""
database_name_description = "用于标识此连接的数据库名称。"
port_description = "数据库连接的端口号。"
cache_timeout_description = (
    "此数据库图表的缓存超时持续时间（秒）。"
    "超时0表示缓存永不过期。"
    "注意：如果未定义，则默认为全局超时。"
)
expose_in_sqllab_description = "将此数据库公开给 SQL Lab"
allow_run_async_description = (
    "以异步模式操作数据库，这意味着查询是在远程工作者上执行的，而不是在web服务器本身上执行的。"
    "这假设您有一个Celery工作者设置以及一个结果后端。有关更多信息，请参阅安装文档。"
)
allow_csv_upload_description = (
    "如果选中允许将CSV文件数据上载到此数据库，请额外设置允许CSV上载的架构。"
)
allow_ctas_description = "在SQL工具箱中允许 CREATE TABLE AS 选项"
allow_cvas_description = "在SQL工具箱中允许 CREATE VIEW AS 选项"
allow_dml_description = (
    "允许用户在 SQL工具箱中运行非-SELECT 语句(UPDATE, DELETE, CREATE, ...) "
)
allow_multi_schema_metadata_fetch_description = (
    "允许SQL Lab获取所有数据库模式中所有表和所有视图的列表。"
    "对于具有数千个表的大型数据仓库，这可能会很昂贵，并给系统带来压力。"
)  # pylint: disable=invalid-name
configuration_method_description = (
    "在前端使用 Configuration_method 通知后端是分解参数还是只提供sqlalchemy_uri。"
)
impersonate_user_description = (
    "如果是Presto，则SQL Lab中的所有查询都将作为当前登录的用户执行，该用户必须具有运行这些查询的权限。"
    "<br/>"
    "如果启用了Hive和Hive.server2.enable.doAs，则将以服务帐户的形式运行查询，"
    "但会通过Hive.server2.proxy.user属性模拟当前登录的用户。"
)
force_ctas_schema_description = (
    "当在SQL Lab中允许 CREATE TABLE AS 选项时, "
    "此选项强制在此模式中创建表"
)
encrypted_extra_description = markdown(
    "包含附加连接配置的JSON字符串。<br/>"
    "这用于为Hive、Presto和BigQuery等系统提供连接信息，这些系统不符合SQLAlchemy通常使用的用户名：密码语法。",
    True,
)
extra_description = markdown(
    "包含额外配置元素的JSON字符串。<br/>"
    "1. ``engine_params`` 对象被提取到 "
    "[sqlalchemy.create_engine]"
    "(https://docs.sqlalchemy.org/en/latest/core/engines.html#"
    "sqlalchemy.create_engine) 调用，而 ``metadata_params`` "
    "被提取到 [sqlalchemy.MetaData]"
    "(https://docs.sqlalchemy.org/en/rel_1_0/core/metadata.html"
    "#sqlalchemy.schema.MetaData) 调用。<br/>"
    "2. ``metadata_cache_timeout`` 是用于获取此数据库元数据的缓存超时设置（以秒为单位）。"
    "指定为 "
    '**"metadata_cache_timeout": {"schema_cache_timeout": 600, '
    '"table_cache_timeout": 600}**. '
    "如果未设置，将不会为该功能启用缓存。"
    "超时0表示缓存永不过期。<br/>"
    "3. ``schemas_allowed_for_csv_upload`` 是允许上传CSV文件的以逗号分隔的模式列表。"
    '指定为 **"schemas_allowed_for_csv_upload": '
    '["public", "csv_upload"]** 。'
    "如果数据库不支持模式或允许访问任何模式，只需将列表留空即可<br/>"
    "4. ``version`` 字段是数据库版本的字符串表示。"
    "这应该与Presto DBs一起使用，以便语法正确<br/>"
    "5. ``allows_virtual_table_explore`` 字段是一个布尔值"
    "指示是否显示SQL工具箱结果中的“浏览”按钮。",
    True,
)
get_export_ids_schema = {"type": "array", "items": {"type": "integer"}}
"""获取导出标识结构"""
sqlalchemy_uri_description = markdown(
    "更多信息参考 "
    "[SqlAlchemy 文档]"
    "(https://docs.sqlalchemy.org/en/rel_1_2/core/engines.html#"
    "database-urls) ",
    True,
)
server_cert_description = markdown(
    "选项 CA_BUNDLE 内容以验证HTTPS请求。"
    "仅在某些数据库引擎上可用。",
    True,
)


def sqlalchemy_uri_validator(value: str) -> str:
    """
    Validate if it's a valid SQLAlchemy URI and refuse SQLLite by default
    """
    try:
        uri = make_url(value.strip())
    except (ArgumentError, AttributeError, ValueError):
        raise ValidationError(
            [
                _(
                    "Invalid connection string, a valid string usually follows: "
                    "driver://user:password@database-host/database-name"
                )
            ]
        )
    if current_app.config.get("PREVENT_UNSAFE_DB_CONNECTIONS", True):
        try:
            check_sqlalchemy_uri(uri)
        except RabbitaiSecurityException as ex:
            raise ValidationError([str(ex)])
    return value


def server_cert_validator(value: str) -> str:
    """
    Validate the server certificate
    """
    if value:
        try:
            parse_ssl_cert(value)
        except CertificateException:
            raise ValidationError([_("Invalid certificate")])
    return value


def encrypted_extra_validator(value: str) -> str:
    """
    Validate that encrypted extra is a valid JSON string
    """
    if value:
        try:
            json.loads(value)
        except json.JSONDecodeError as ex:
            raise ValidationError(
                [_("Field cannot be decoded by JSON. %(msg)s", msg=str(ex))]
            )
    return value


def extra_validator(value: str) -> str:
    """
    Validate that extra is a valid JSON string, and that metadata_params
    keys are on the call signature for SQLAlchemy Metadata
    """

    if value:
        try:
            extra_ = json.loads(value)
        except json.JSONDecodeError as ex:
            raise ValidationError(
                [_("Field cannot be decoded by JSON. %(msg)s", msg=str(ex))]
            )
        else:
            metadata_signature = inspect.signature(MetaData)
            for key in extra_.get("metadata_params", {}):
                if key not in metadata_signature.parameters:
                    raise ValidationError(
                        [
                            _(
                                "The metadata_params in Extra field "
                                "is not configured correctly. The key "
                                "%(key)s is invalid.",
                                key=key,
                            )
                        ]
                    )
    return value


class DatabaseParametersSchemaMixin:
    """
    Allow SQLAlchemy URI to be passed as separate parameters.

    This mixin is a first step in allowing the users to test, create and
    edit databases without having to know how to write a SQLAlchemy URI.
    Instead, each database defines the parameters that it takes (eg,
    username, password, host, etc.) and the SQLAlchemy URI is built from
    these parameters.

    When using this mixin make sure that `sqlalchemy_uri` is not required.
    """

    engine = fields.String(allow_none=True, description="SQLAlchemy 引擎")
    parameters = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(),
        description="用于配置的数据库特定参数",
    )
    configuration_method = EnumField(
        ConfigurationMethod,
        by_value=True,
        description=configuration_method_description,
        missing=ConfigurationMethod.SQLALCHEMY_FORM,
    )

    @pre_load
    def build_sqlalchemy_uri(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Build SQLAlchemy URI from separate parameters.

        This is used for databases that support being configured by individual
        parameters (eg, username, password, host, etc.), instead of requiring
        the constructed SQLAlchemy URI to be passed.
        """

        parameters = data.pop("parameters", {})

        engine = (
            data.pop("engine", None)
            or parameters.pop("engine", None)
            or data.pop("backend", None)
        )

        configuration_method = data.get("configuration_method")
        if configuration_method == ConfigurationMethod.DYNAMIC_FORM:
            engine_spec = get_engine_spec(engine)

            if not hasattr(engine_spec, "build_sqlalchemy_uri") or not hasattr(
                engine_spec, "parameters_schema"
            ):
                raise ValidationError(
                    [
                        _(
                            'Engine spec "InvalidEngine" does not support '
                            "being configured via individual parameters."
                        )
                    ]
                )

            # validate parameters
            parameters = engine_spec.parameters_schema.load(parameters)

            serialized_encrypted_extra = data.get("encrypted_extra") or "{}"
            try:
                encrypted_extra = json.loads(serialized_encrypted_extra)
            except json.decoder.JSONDecodeError:
                encrypted_extra = {}

            data["sqlalchemy_uri"] = engine_spec.build_sqlalchemy_uri(
                parameters, encrypted_extra
            )

        return data


def get_engine_spec(engine: Optional[str]) -> Type[BaseEngineSpec]:
    """
    获取数据库引擎规范 BaseEngineSpec。

    :param engine: 引擎名称。

    :return: 数据库引擎规范 BaseEngineSpec。
    """

    if not engine:
        raise ValidationError(
            [
                _(
                    "An engine must be specified when passing "
                    "individual parameters to a database."
                )
            ]
        )
    engine_specs = get_engine_specs()
    if engine not in engine_specs:
        raise ValidationError(
            [_('Engine "%(engine)s" is not a valid engine.', engine=engine,)]
        )
    return engine_specs[engine]


class DatabaseValidateParametersSchema(Schema):
    """数据库验证参数结构。"""

    class Meta:  # pylint: disable=too-few-public-methods
        unknown = EXCLUDE

    engine = fields.String(required=True, description="SQLAlchemy 引擎")
    parameters = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(allow_none=True),
        description="用于配置的数据库特定参数",
    )
    database_name = fields.String(
        description=database_name_description, allow_none=True, validate=Length(1, 250),
    )
    impersonate_user = fields.Boolean(description=impersonate_user_description)
    extra = fields.String(description=extra_description, validate=extra_validator)
    encrypted_extra = fields.String(
        description=encrypted_extra_description,
        validate=encrypted_extra_validator,
        allow_none=True,
    )
    server_cert = fields.String(
        description=server_cert_description,
        allow_none=True,
        validate=server_cert_validator,
    )
    configuration_method = EnumField(
        ConfigurationMethod,
        by_value=True,
        required=True,
        description=configuration_method_description,
    )


class DatabasePostSchema(Schema, DatabaseParametersSchemaMixin):
    """新建数据库对象模型结构。"""

    class Meta:  # pylint: disable=too-few-public-methods
        unknown = EXCLUDE

    database_name = fields.String(
        description=database_name_description, required=True, validate=Length(1, 250),
    )
    cache_timeout = fields.Integer(
        description=cache_timeout_description, allow_none=True
    )
    expose_in_sqllab = fields.Boolean(description=expose_in_sqllab_description)
    allow_run_async = fields.Boolean(description=allow_run_async_description)
    allow_csv_upload = fields.Boolean(description=allow_csv_upload_description)
    allow_ctas = fields.Boolean(description=allow_ctas_description)
    allow_cvas = fields.Boolean(description=allow_cvas_description)
    allow_dml = fields.Boolean(description=allow_dml_description)
    force_ctas_schema = fields.String(
        description=force_ctas_schema_description,
        allow_none=True,
        validate=Length(0, 250),
    )
    allow_multi_schema_metadata_fetch = fields.Boolean(
        description=allow_multi_schema_metadata_fetch_description,
    )
    impersonate_user = fields.Boolean(description=impersonate_user_description)
    encrypted_extra = fields.String(
        description=encrypted_extra_description,
        validate=encrypted_extra_validator,
        allow_none=True,
    )
    extra = fields.String(description=extra_description, validate=extra_validator)
    server_cert = fields.String(
        description=server_cert_description,
        allow_none=True,
        validate=server_cert_validator,
    )
    sqlalchemy_uri = fields.String(
        description=sqlalchemy_uri_description,
        validate=[Length(1, 1024), sqlalchemy_uri_validator],
    )


class DatabasePutSchema(Schema, DatabaseParametersSchemaMixin):
    """更新数据库对象模型结构。"""

    class Meta:  # pylint: disable=too-few-public-methods
        unknown = EXCLUDE

    database_name = fields.String(
        description=database_name_description, allow_none=True, validate=Length(1, 250),
    )
    cache_timeout = fields.Integer(
        description=cache_timeout_description, allow_none=True
    )
    expose_in_sqllab = fields.Boolean(description=expose_in_sqllab_description)
    allow_run_async = fields.Boolean(description=allow_run_async_description)
    allow_csv_upload = fields.Boolean(description=allow_csv_upload_description)
    allow_ctas = fields.Boolean(description=allow_ctas_description)
    allow_cvas = fields.Boolean(description=allow_cvas_description)
    allow_dml = fields.Boolean(description=allow_dml_description)
    force_ctas_schema = fields.String(
        description=force_ctas_schema_description,
        allow_none=True,
        validate=Length(0, 250),
    )
    allow_multi_schema_metadata_fetch = fields.Boolean(
        description=allow_multi_schema_metadata_fetch_description
    )
    impersonate_user = fields.Boolean(description=impersonate_user_description)
    encrypted_extra = fields.String(
        description=encrypted_extra_description,
        allow_none=True,
        validate=encrypted_extra_validator,
    )
    extra = fields.String(description=extra_description, validate=extra_validator)
    server_cert = fields.String(
        description=server_cert_description,
        allow_none=True,
        validate=server_cert_validator,
    )
    sqlalchemy_uri = fields.String(
        description=sqlalchemy_uri_description,
        validate=[Length(0, 1024), sqlalchemy_uri_validator],
    )


class DatabaseTestConnectionSchema(Schema, DatabaseParametersSchemaMixin):
    """数据库测试连接结构。"""

    database_name = fields.String(
        description=database_name_description, allow_none=True, validate=Length(1, 250),
    )
    impersonate_user = fields.Boolean(description=impersonate_user_description)
    extra = fields.String(description=extra_description, validate=extra_validator)
    encrypted_extra = fields.String(
        description=encrypted_extra_description,
        validate=encrypted_extra_validator,
        allow_none=True,
    )
    server_cert = fields.String(
        description=server_cert_description,
        allow_none=True,
        validate=server_cert_validator,
    )
    sqlalchemy_uri = fields.String(
        description=sqlalchemy_uri_description,
        validate=[Length(1, 1024), sqlalchemy_uri_validator],
    )


class TableMetadataOptionsResponseSchema(Schema):
    """数据表元数据选项响应结构。"""
    deferrable = fields.Bool()
    initially = fields.Bool()
    match = fields.Bool()
    ondelete = fields.Bool()
    onupdate = fields.Bool()


class TableMetadataColumnsResponseSchema(Schema):
    """数据表元数据列响应结构。"""
    keys = fields.List(fields.String(), description="")
    longType = fields.String(description="列的实际后端长类型")
    name = fields.String(description="列名称")
    type = fields.String(description="列数据类型")
    duplicates_constraint = fields.String(required=False)


class TableMetadataForeignKeysIndexesResponseSchema(Schema):
    column_names = fields.List(
        fields.String(
            description="组成外键或索引的列名列表"
        )
    )
    name = fields.String(description="外键或索引的名称")
    options = fields.Nested(TableMetadataOptionsResponseSchema)
    referred_columns = fields.List(fields.String())
    referred_schema = fields.String()
    referred_table = fields.String()
    type = fields.String()


class TableMetadataPrimaryKeyResponseSchema(Schema):
    column_names = fields.List(
        fields.String(description="组成主键的列名列表")
    )
    name = fields.String(description="主键名称")
    type = fields.String()


class TableMetadataResponseSchema(Schema):
    name = fields.String(description="数据表名称")
    columns = fields.List(
        fields.Nested(TableMetadataColumnsResponseSchema),
        description="列及其元数据的列表",
    )
    foreignKeys = fields.List(
        fields.Nested(TableMetadataForeignKeysIndexesResponseSchema),
        description="外键及其元数据的列表",
    )
    indexes = fields.List(
        fields.Nested(TableMetadataForeignKeysIndexesResponseSchema),
        description="索引及其元数据的列表",
    )
    primaryKey = fields.Nested(
        TableMetadataPrimaryKeyResponseSchema, description="主键元数据"
    )
    selectStar = fields.String(description="SQL SELECT *")


class SelectStarResponseSchema(Schema):
    result = fields.String(description="SQL SELECT *")


class SchemasResponseSchema(Schema):
    result = fields.List(fields.String(description="数据库模式名称"))


class DatabaseRelatedChart(Schema):
    id = fields.Integer()
    slice_name = fields.String()
    viz_type = fields.String()


class DatabaseRelatedDashboard(Schema):
    id = fields.Integer()
    json_metadata = fields.Dict()
    slug = fields.String()
    title = fields.String()


class DatabaseRelatedCharts(Schema):
    count = fields.Integer(description="图表数")
    result = fields.List(
        fields.Nested(DatabaseRelatedChart), description="仪表盘的列表"
    )


class DatabaseRelatedDashboards(Schema):
    count = fields.Integer(description="仪表盘数")
    result = fields.List(
        fields.Nested(DatabaseRelatedDashboard), description="仪表盘的列表"
    )


class DatabaseRelatedObjectsResponse(Schema):
    charts = fields.Nested(DatabaseRelatedCharts)
    dashboards = fields.Nested(DatabaseRelatedDashboards)


class DatabaseFunctionNamesResponse(Schema):
    function_names = fields.List(fields.String())


class ImportV1DatabaseExtraSchema(Schema):
    # pylint: disable=no-self-use, unused-argument
    @pre_load
    def fix_schemas_allowed_for_csv_upload(
        self, data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Fix ``schemas_allowed_for_csv_upload`` being a string.

        Due to a bug in the database modal, some databases might have been
        saved and exported with a string for ``schemas_allowed_for_csv_upload``.
        """
        schemas_allowed_for_csv_upload = data.get("schemas_allowed_for_csv_upload")
        if isinstance(schemas_allowed_for_csv_upload, str):
            data["schemas_allowed_for_csv_upload"] = json.loads(
                schemas_allowed_for_csv_upload
            )

        return data

    metadata_params = fields.Dict(keys=fields.Str(), values=fields.Raw())
    engine_params = fields.Dict(keys=fields.Str(), values=fields.Raw())
    metadata_cache_timeout = fields.Dict(keys=fields.Str(), values=fields.Integer())
    schemas_allowed_for_csv_upload = fields.List(fields.String())
    cost_estimate_enabled = fields.Boolean()


class ImportV1DatabaseSchema(Schema):
    database_name = fields.String(required=True)
    sqlalchemy_uri = fields.String(required=True)
    password = fields.String(allow_none=True)
    cache_timeout = fields.Integer(allow_none=True)
    expose_in_sqllab = fields.Boolean()
    allow_run_async = fields.Boolean()
    allow_ctas = fields.Boolean()
    allow_cvas = fields.Boolean()
    allow_csv_upload = fields.Boolean()
    extra = fields.Nested(ImportV1DatabaseExtraSchema)
    uuid = fields.UUID(required=True)
    version = fields.String(required=True)

    # pylint: disable=no-self-use, unused-argument
    @validates_schema
    def validate_password(self, data: Dict[str, Any], **kwargs: Any) -> None:
        """If sqlalchemy_uri has a masked password, password is required"""
        uri = data["sqlalchemy_uri"]
        password = make_url(uri).password
        if password == PASSWORD_MASK and data.get("password") is None:
            raise ValidationError("Must provide a password for the database")


class EncryptedField(fields.String):
    """加密的字段"""
    pass


def encrypted_field_properties(self, field: Any, **_) -> Dict[str, Any]:
    """

    :param self:
    :param field:
    :param _:
    :return:
    """

    ret = {}
    if isinstance(field, EncryptedField):
        if self.openapi_version.major > 2:
            ret["x-encrypted-extra"] = True
    return ret
