import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Pattern, Tuple, TYPE_CHECKING

from flask_babel import gettext as __
from sqlalchemy.engine.reflection import Inspector

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.errors import RabbitaiErrorType
from rabbitai.utils import core as utils

if TYPE_CHECKING:
    # prevent circular imports
    from rabbitai.models.core import Database


COLUMN_DOES_NOT_EXIST_REGEX = re.compile("no such column: (?P<column_name>.+)")


class SqliteEngineSpec(BaseEngineSpec):
    """SQLite 数据库引擎规范。"""

    engine = "sqlite"
    engine_name = "SQLite"

    # pylint: disable=line-too-long
    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "DATETIME(STRFTIME('%Y-%m-%dT%H:%M:%S', {col}))",
        "PT1M": "DATETIME(STRFTIME('%Y-%m-%dT%H:%M:00', {col}))",
        "PT1H": "DATETIME(STRFTIME('%Y-%m-%dT%H:00:00', {col}))",
        "P1D": "DATE({col})",
        "P1W": "DATE({col}, -strftime('%W', {col}) || ' days')",
        "P1M": "DATE({col}, -strftime('%d', {col}) || ' days', '+1 day')",
        "P0.25Y": (
            "DATETIME(STRFTIME('%Y-', {col}) || "  # year
            "SUBSTR('00' || "  # pad with zeros to 2 chars
            "((CAST(STRFTIME('%m', {col}) AS INTEGER)) - "  # month as integer
            "(((CAST(STRFTIME('%m', {col}) AS INTEGER)) - 1) % 3)), "  # month in quarter
            "-2) || "  # close pad
            "'-01T00:00:00')"
        ),
        "P1Y": "DATETIME(STRFTIME('%Y-01-01T00:00:00', {col}))",
        "P1W/1970-01-03T00:00:00Z": "DATE({col}, 'weekday 6')",
        "1969-12-28T00:00:00Z/P1W": "DATE({col}, 'weekday 0', '-7 days')",
    }

    custom_errors: Dict[Pattern[str], Tuple[str, RabbitaiErrorType, Dict[str, Any]]] = {
        COLUMN_DOES_NOT_EXIST_REGEX: (
            __('We can\'t seem to resolve the column "%(column_name)s"'),
            RabbitaiErrorType.COLUMN_DOES_NOT_EXIST_ERROR,
            {},
        ),
    }

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "datetime({col}, 'unixepoch')"

    @classmethod
    def get_all_datasource_names(
        cls, database: "Database", datasource_type: str
    ) -> List[utils.DatasourceName]:
        schemas = database.get_all_schema_names(
            cache=database.schema_cache_enabled,
            cache_timeout=database.schema_cache_timeout,
            force=True,
        )
        schema = schemas[0]
        if datasource_type == "table":
            return database.get_all_table_names_in_schema(
                schema=schema,
                force=True,
                cache=database.table_cache_enabled,
                cache_timeout=database.table_cache_timeout,
            )
        if datasource_type == "view":
            return database.get_all_view_names_in_schema(
                schema=schema,
                force=True,
                cache=database.table_cache_enabled,
                cache_timeout=database.table_cache_timeout,
            )
        raise Exception(f"Unsupported datasource_type: {datasource_type}")

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt in (utils.TemporalType.TEXT, utils.TemporalType.DATETIME):
            return f"""'{dttm.isoformat(sep=" ", timespec="microseconds")}'"""
        return None

    @classmethod
    def get_table_names(
        cls, database: "Database", inspector: Inspector, schema: Optional[str]
    ) -> List[str]:
        """
        获取数据表名称的列表。

        :param database:
        :param inspector:
        :param schema:
        :return:
        """
        return sorted(inspector.get_table_names())
