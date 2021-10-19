from contextlib import closing
from typing import Dict, List, Optional, TYPE_CHECKING

from flask_babel import lazy_gettext as _
from sqlalchemy.sql.type_api import TypeEngine

from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import (
    RabbitaiGenericDBErrorException,
    RabbitaiSecurityException,
)
from rabbitai.models.core import Database
from rabbitai.result_set import RabbitaiResultSet
from rabbitai.sql_parse import ParsedQuery

if TYPE_CHECKING:
    from rabbitai.connectors.sqla.models import SqlaTable


def get_physical_table_metadata(
    database: Database, table_name: str, schema_name: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Use SQLAlchemy inspector to get table metadata"""
    db_engine_spec = database.db_engine_spec
    db_dialect = database.get_dialect()
    # ensure empty schema
    _schema_name = schema_name if schema_name else None
    cols = database.get_columns(table_name, schema=_schema_name)
    for col in cols:
        try:
            if isinstance(col["type"], TypeEngine):
                db_type = db_engine_spec.column_datatype_to_string(
                    col["type"], db_dialect
                )
                type_spec = db_engine_spec.get_column_spec(db_type)
                col.update(
                    {
                        "type": db_type,
                        "type_generic": type_spec.generic_type if type_spec else None,
                        "is_dttm": type_spec.is_dttm if type_spec else None,
                    }
                )
        # Broad exception catch, because there are multiple possible exceptions
        # from different drivers that fall outside CompileError
        except Exception:  # pylint: disable=broad-except
            col.update(
                {"type": "UNKNOWN", "generic_type": None, "is_dttm": None,}
            )
    return cols


def get_virtual_table_metadata(dataset: "SqlaTable") -> List[Dict[str, str]]:
    """Use SQLparser to get virtual dataset metadata"""
    if not dataset.sql:
        raise RabbitaiGenericDBErrorException(
            message=_("Virtual dataset query cannot be empty"),
        )

    db_engine_spec = dataset.database.db_engine_spec
    engine = dataset.database.get_sqla_engine(schema=dataset.schema)
    sql = dataset.get_template_processor().process_template(
        dataset.sql, **dataset.template_params_dict
    )
    parsed_query = ParsedQuery(sql)
    if not db_engine_spec.is_readonly_query(parsed_query):
        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.DATASOURCE_SECURITY_ACCESS_ERROR,
                message=_("Only `SELECT` statements are allowed"),
                level=ErrorLevel.ERROR,
            )
        )
    statements = parsed_query.get_statements()
    if len(statements) > 1:
        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.DATASOURCE_SECURITY_ACCESS_ERROR,
                message=_("Only single queries supported"),
                level=ErrorLevel.ERROR,
            )
        )
    # TODO(villebro): refactor to use same code that's used by
    #  sql_lab.py:execute_sql_statements
    try:
        with closing(engine.raw_connection()) as conn:
            cursor = conn.cursor()
            query = dataset.database.apply_limit_to_sql(statements[0])
            db_engine_spec.execute(cursor, query)
            result = db_engine_spec.fetch_data(cursor, limit=1)
            result_set = RabbitaiResultSet(result, cursor.description, db_engine_spec)
            cols = result_set.columns
    except Exception as exc:
        raise RabbitaiGenericDBErrorException(message=str(exc))
    return cols
