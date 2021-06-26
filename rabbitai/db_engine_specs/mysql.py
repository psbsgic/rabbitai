import re
from datetime import datetime
from typing import Any, Callable, Dict, Match, Optional, Pattern, Tuple, Union
from urllib import parse

from flask_babel import gettext as __
from sqlalchemy.dialects.mysql import (
    BIT,
    DECIMAL,
    DOUBLE,
    FLOAT,
    INTEGER,
    LONGTEXT,
    MEDIUMINT,
    MEDIUMTEXT,
    TINYINT,
    TINYTEXT,
)
from sqlalchemy.engine.url import URL
from sqlalchemy.types import TypeEngine

from rabbitai.db_engine_specs.base import BaseEngineSpec, BasicParametersMixin
from rabbitai.errors import RabbitaiErrorType
from rabbitai.utils import core as utils
from rabbitai.utils.core import ColumnSpec, GenericDataType

# Regular expressions to catch custom errors
CONNECTION_ACCESS_DENIED_REGEX = re.compile(
    "Access denied for user '(?P<username>.*?)'@'(?P<hostname>.*?)'"
)
CONNECTION_INVALID_HOSTNAME_REGEX = re.compile(
    "Unknown MySQL server host '(?P<hostname>.*?)'"
)
CONNECTION_HOST_DOWN_REGEX = re.compile(
    "Can't connect to MySQL server on '(?P<hostname>.*?)'"
)
CONNECTION_UNKNOWN_DATABASE_REGEX = re.compile("Unknown database '(?P<database>.*?)'")


class MySQLEngineSpec(BaseEngineSpec, BasicParametersMixin):
    engine = "mysql"
    engine_name = "MySQL"
    max_column_name_length = 64

    default_driver = "mysqldb"
    sqlalchemy_uri_placeholder = (
        "mysql://user:password@host:port/dbname[?key=value&key=value...]"
    )
    encryption_parameters = {"ssl": "1"}

    column_type_mappings: Tuple[
        Tuple[
            Pattern[str],
            Union[TypeEngine, Callable[[Match[str]], TypeEngine]],
            GenericDataType,
        ],
        ...,
    ] = (
        (re.compile(r"^int.*", re.IGNORECASE), INTEGER(), GenericDataType.NUMERIC,),
        (re.compile(r"^tinyint", re.IGNORECASE), TINYINT(), GenericDataType.NUMERIC,),
        (
            re.compile(r"^mediumint", re.IGNORECASE),
            MEDIUMINT(),
            GenericDataType.NUMERIC,
        ),
        (re.compile(r"^decimal", re.IGNORECASE), DECIMAL(), GenericDataType.NUMERIC,),
        (re.compile(r"^float", re.IGNORECASE), FLOAT(), GenericDataType.NUMERIC,),
        (re.compile(r"^double", re.IGNORECASE), DOUBLE(), GenericDataType.NUMERIC,),
        (re.compile(r"^bit", re.IGNORECASE), BIT(), GenericDataType.NUMERIC,),
        (re.compile(r"^tinytext", re.IGNORECASE), TINYTEXT(), GenericDataType.STRING,),
        (
            re.compile(r"^mediumtext", re.IGNORECASE),
            MEDIUMTEXT(),
            GenericDataType.STRING,
        ),
        (re.compile(r"^longtext", re.IGNORECASE), LONGTEXT(), GenericDataType.STRING,),
    )

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "DATE_ADD(DATE({col}), "
        "INTERVAL (HOUR({col})*60*60 + MINUTE({col})*60"
        " + SECOND({col})) SECOND)",
        "PT1M": "DATE_ADD(DATE({col}), "
        "INTERVAL (HOUR({col})*60 + MINUTE({col})) MINUTE)",
        "PT1H": "DATE_ADD(DATE({col}), " "INTERVAL HOUR({col}) HOUR)",
        "P1D": "DATE({col})",
        "P1W": "DATE(DATE_SUB({col}, " "INTERVAL DAYOFWEEK({col}) - 1 DAY))",
        "P1M": "DATE(DATE_SUB({col}, " "INTERVAL DAYOFMONTH({col}) - 1 DAY))",
        "P0.25Y": "MAKEDATE(YEAR({col}), 1) "
        "+ INTERVAL QUARTER({col}) QUARTER - INTERVAL 1 QUARTER",
        "P1Y": "DATE(DATE_SUB({col}, " "INTERVAL DAYOFYEAR({col}) - 1 DAY))",
        "1969-12-29T00:00:00Z/P1W": "DATE(DATE_SUB({col}, "
        "INTERVAL DAYOFWEEK(DATE_SUB({col}, "
        "INTERVAL 1 DAY)) - 1 DAY))",
    }

    type_code_map: Dict[int, str] = {}  # loaded from get_datatype only if needed

    custom_errors: Dict[Pattern[str], Tuple[str, RabbitaiErrorType, Dict[str, Any]]] = {
        CONNECTION_ACCESS_DENIED_REGEX: (
            __('Either the username "%(username)s" or the password is incorrect.'),
            RabbitaiErrorType.CONNECTION_ACCESS_DENIED_ERROR,
            {"invalid": ["username", "password"]},
        ),
        CONNECTION_INVALID_HOSTNAME_REGEX: (
            __('Unknown MySQL server host "%(hostname)s".'),
            RabbitaiErrorType.CONNECTION_INVALID_HOSTNAME_ERROR,
            {"invalid": ["host"]},
        ),
        CONNECTION_HOST_DOWN_REGEX: (
            __('The host "%(hostname)s" might be down and can\'t be reached.'),
            RabbitaiErrorType.CONNECTION_HOST_DOWN_ERROR,
            {"invalid": ["host", "port"]},
        ),
        CONNECTION_UNKNOWN_DATABASE_REGEX: (
            __('Unable to connect to database "%(database)s".'),
            RabbitaiErrorType.CONNECTION_UNKNOWN_DATABASE_ERROR,
            {"invalid": ["database"]},
        ),
    }

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.DATE:
            return f"STR_TO_DATE('{dttm.date().isoformat()}', '%Y-%m-%d')"
        if tt == utils.TemporalType.DATETIME:
            datetime_formatted = dttm.isoformat(sep=" ", timespec="microseconds")
            return f"""STR_TO_DATE('{datetime_formatted}', '%Y-%m-%d %H:%i:%s.%f')"""
        return None

    @classmethod
    def adjust_database_uri(
        cls, uri: URL, selected_schema: Optional[str] = None
    ) -> None:
        if selected_schema:
            uri.database = parse.quote(selected_schema, safe="")

    @classmethod
    def get_datatype(cls, type_code: Any) -> Optional[str]:
        if not cls.type_code_map:
            # only import and store if needed at least once
            import MySQLdb

            ft = MySQLdb.constants.FIELD_TYPE
            cls.type_code_map = {
                getattr(ft, k): k for k in dir(ft) if not k.startswith("_")
            }
        datatype = type_code
        if isinstance(type_code, int):
            datatype = cls.type_code_map.get(type_code)
        if datatype and isinstance(datatype, str) and datatype:
            return datatype
        return None

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "from_unixtime({col})"

    @classmethod
    def _extract_error_message(cls, ex: Exception) -> str:
        """Extract error message for queries"""
        message = str(ex)
        try:
            if isinstance(ex.args, tuple) and len(ex.args) > 1:
                message = ex.args[1]
        except (AttributeError, KeyError):
            pass
        return message

    @classmethod
    def get_column_spec(  # type: ignore
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

        column_spec = super().get_column_spec(native_type)
        if column_spec:
            return column_spec

        return super().get_column_spec(
            native_type, column_type_mappings=column_type_mappings
        )