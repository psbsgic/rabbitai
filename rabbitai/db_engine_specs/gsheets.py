import json
import re
from contextlib import closing
from typing import Any, Dict, List, Optional, Pattern, Tuple, TYPE_CHECKING

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import g
from flask_babel import gettext as __
from marshmallow import fields, Schema
from marshmallow.exceptions import ValidationError
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from typing_extensions import TypedDict

from rabbitai import security_manager
from rabbitai.databases.schemas import encrypted_field_properties
from rabbitai.db_engine_specs.sqlite import SqliteEngineSpec
from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType

if TYPE_CHECKING:
    from rabbitai.models.core import Database


SYNTAX_ERROR_REGEX = re.compile('SQLError: near "(?P<server_error>.*?)": syntax error')

ma_plugin = MarshmallowPlugin()


class GSheetsParametersSchema(Schema):
    catalog = fields.Dict()


class GSheetsParametersType(TypedDict):
    credentials_info: Dict[str, Any]
    catalog: Dict[str, str]


class GSheetsEngineSpec(SqliteEngineSpec):
    """Engine for Google spreadsheets"""

    engine = "gsheets"
    engine_name = "Google Sheets"
    allows_joins = True
    allows_subqueries = True

    parameters_schema = GSheetsParametersSchema()
    default_driver = "apsw"
    sqlalchemy_uri_placeholder = "gsheets://"

    custom_errors: Dict[Pattern[str], Tuple[str, RabbitaiErrorType, Dict[str, Any]]] = {
        SYNTAX_ERROR_REGEX: (
            __(
                'Please check your query for syntax errors near "%(server_error)s". '
                "Then, try running your query again.",
            ),
            RabbitaiErrorType.SYNTAX_ERROR,
            {},
        ),
    }

    @classmethod
    def modify_url_for_impersonation(
        cls, url: URL, impersonate_user: bool, username: Optional[str],
    ) -> None:
        if impersonate_user and username is not None:
            user = security_manager.find_user(username=username)
            if user and user.email:
                url.query["subject"] = user.email

    @classmethod
    def extra_table_metadata(
        cls, database: "Database", table_name: str, schema_name: str,
    ) -> Dict[str, Any]:
        engine = cls.get_engine(database, schema=schema_name)
        with closing(engine.raw_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT GET_METADATA("{table_name}")')
            results = cursor.fetchone()[0]

        try:
            metadata = json.loads(results)
        except Exception:  # pylint: disable=broad-except
            metadata = {}

        return {"metadata": metadata["extra"]}

    @classmethod
    def build_sqlalchemy_uri(
        cls,
        _: GSheetsParametersType,
        encrypted_extra: Optional[  # pylint: disable=unused-argument
            Dict[str, Any]
        ] = None,
    ) -> str:  # pylint: disable=unused-variable

        return "gsheets://"

    @classmethod
    def get_parameters_from_uri(
        cls, encrypted_extra: Optional[Dict[str, str]] = None,
    ) -> Any:
        # Building parameters from encrypted_extra and uri
        if encrypted_extra:
            return {**encrypted_extra}

        raise ValidationError("Invalid service credentials")

    @classmethod
    def parameters_json_schema(cls) -> Any:
        """
        Return configuration parameters as OpenAPI.
        """
        if not cls.parameters_schema:
            return None

        spec = APISpec(
            title="Database Parameters",
            version="1.0.0",
            openapi_version="3.0.0",
            plugins=[ma_plugin],
        )

        ma_plugin.init_spec(spec)
        ma_plugin.converter.add_attribute_function(encrypted_field_properties)
        spec.components.schema(cls.__name__, schema=cls.parameters_schema)
        return spec.to_dict()["components"]["schemas"][cls.__name__]

    @classmethod
    def validate_parameters(
        cls, parameters: GSheetsParametersType,
    ) -> List[RabbitaiError]:
        errors: List[RabbitaiError] = []
        credentials_info = parameters.get("credentials_info")
        table_catalog = parameters.get("catalog", {})

        if not table_catalog:
            errors.append(
                RabbitaiError(
                    message="URL is required",
                    error_type=RabbitaiErrorType.CONNECTION_MISSING_PARAMETERS_ERROR,
                    level=ErrorLevel.WARNING,
                    extra={"invalid": ["catalog"], "name": "", "url": ""},
                ),
            )
            return errors

        # We need a subject in case domain wide delegation is set, otherwise the
        # check will fail. This means that the admin will be able to add sheets
        # that only they have access, even if later users are not able to access
        # them.
        subject = g.user.email if g.user else None

        engine = create_engine(
            "gsheets://", service_account_info=credentials_info, subject=subject,
        )
        conn = engine.connect()
        for name, url in table_catalog.items():

            if not name:
                errors.append(
                    RabbitaiError(
                        message="Sheet name is required",
                        error_type=RabbitaiErrorType.CONNECTION_MISSING_PARAMETERS_ERROR,
                        level=ErrorLevel.WARNING,
                        extra={"invalid": [], "name": name, "url": url},
                    ),
                )

            try:
                results = conn.execute(f'SELECT * FROM "{url}" LIMIT 1')
                results.fetchall()
            except Exception:  # pylint: disable=broad-except
                errors.append(
                    RabbitaiError(
                        message="URL could not be identified",
                        error_type=RabbitaiErrorType.TABLE_DOES_NOT_EXIST_ERROR,
                        level=ErrorLevel.WARNING,
                        extra={"invalid": ["catalog"], "name": name, "url": url},
                    ),
                )
        return errors
