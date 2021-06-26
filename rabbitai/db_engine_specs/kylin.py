from datetime import datetime
from typing import Optional

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.utils import core as utils


class KylinEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    """Dialect for Apache Kylin"""

    engine = "kylin"
    engine_name = "Apache Kylin"

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO SECOND) AS TIMESTAMP)",
        "PT1M": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO MINUTE) AS TIMESTAMP)",
        "PT1H": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO HOUR) AS TIMESTAMP)",
        "P1D": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO DAY) AS DATE)",
        "P1W": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO WEEK) AS DATE)",
        "P1M": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO MONTH) AS DATE)",
        "P0.25Y": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO QUARTER) AS DATE)",
        "P1Y": "CAST(FLOOR(CAST({col} AS TIMESTAMP) TO YEAR) AS DATE)",
    }

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.DATE:
            return f"CAST('{dttm.date().isoformat()}' AS DATE)"
        if tt == utils.TemporalType.TIMESTAMP:
            datetime_fomatted = dttm.isoformat(sep=" ", timespec="seconds")
            return f"""CAST('{datetime_fomatted}' AS TIMESTAMP)"""
        return None
