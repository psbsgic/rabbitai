from typing import Any, List, Optional, Tuple

from rabbitai.db_engine_specs.base import BaseEngineSpec


class ExasolEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    """Engine spec for Exasol"""

    engine = "exa"
    engine_name = "Exasol"
    max_column_name_length = 128

    # Exasol's DATE_TRUNC function is PostgresSQL compatible
    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "DATE_TRUNC('second', {col})",
        "PT1M": "DATE_TRUNC('minute', {col})",
        "PT1H": "DATE_TRUNC('hour', {col})",
        "P1D": "DATE_TRUNC('day', {col})",
        "P1W": "DATE_TRUNC('week', {col})",
        "P1M": "DATE_TRUNC('month', {col})",
        "P0.25Y": "DATE_TRUNC('quarter', {col})",
        "P1Y": "DATE_TRUNC('year', {col})",
    }

    @classmethod
    def fetch_data(
        cls, cursor: Any, limit: Optional[int] = None
    ) -> List[Tuple[Any, ...]]:
        data = super().fetch_data(cursor, limit)
        # Lists of `pyodbc.Row` need to be unpacked further
        return cls.pyodbc_rows_to_tuples(data)
