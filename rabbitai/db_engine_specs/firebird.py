from datetime import datetime
from typing import Optional

from rabbitai.db_engine_specs.base import BaseEngineSpec, LimitMethod
from rabbitai.utils import core as utils


class FirebirdEngineSpec(BaseEngineSpec):
    """Engine for Firebird"""

    engine = "firebird"
    engine_name = "Firebird"

    # Firebird uses FIRST to limit: `SELECT FIRST 10 * FROM table`
    limit_method = LimitMethod.FETCH_MANY

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": (
            "CAST(CAST({col} AS DATE) "
            "|| ' ' "
            "|| EXTRACT(HOUR FROM {col}) "
            "|| ':' "
            "|| EXTRACT(MINUTE FROM {col}) "
            "|| ':' "
            "|| FLOOR(EXTRACT(SECOND FROM {col})) AS TIMESTAMP)"
        ),
        "PT1M": (
            "CAST(CAST({col} AS DATE) "
            "|| ' ' "
            "|| EXTRACT(HOUR FROM {col}) "
            "|| ':' "
            "|| EXTRACT(MINUTE FROM {col}) "
            "|| ':00' AS TIMESTAMP)"
        ),
        "PT1H": (
            "CAST(CAST({col} AS DATE) "
            "|| ' ' "
            "|| EXTRACT(HOUR FROM {col}) "
            "|| ':00:00' AS TIMESTAMP)"
        ),
        "P1D": "CAST({col} AS DATE)",
        "P1M": (
            "CAST(EXTRACT(YEAR FROM {col}) "
            "|| '-' "
            "|| EXTRACT(MONTH FROM {col}) "
            "|| '-01' AS DATE)"
        ),
        "P1Y": "CAST(EXTRACT(YEAR FROM {col}) || '-01-01' AS DATE)",
    }

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "DATEADD(second, {col}, CAST('00:00:00' AS TIMESTAMP))"

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.TIMESTAMP:
            dttm_formatted = dttm.isoformat(sep=" ")
            dttm_valid_precision = dttm_formatted[: len("YYYY-MM-DD HH:MM:SS.MMMM")]
            return f"CAST('{dttm_valid_precision}' AS TIMESTAMP)"
        if tt == utils.TemporalType.DATE:
            return f"CAST('{dttm.date().isoformat()}' AS DATE)"
        if tt == utils.TemporalType.TIME:
            return f"CAST('{dttm.time().isoformat()}' AS TIME)"
        return None
