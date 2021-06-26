from datetime import datetime
from typing import List, Optional

from sqlalchemy.engine.reflection import Inspector

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.utils import core as utils


class ImpalaEngineSpec(BaseEngineSpec):
    """Engine spec for Cloudera's Impala"""

    engine = "impala"
    engine_name = "Apache Impala"

    _time_grain_expressions = {
        None: "{col}",
        "PT1M": "TRUNC({col}, 'MI')",
        "PT1H": "TRUNC({col}, 'HH')",
        "P1D": "TRUNC({col}, 'DD')",
        "P1W": "TRUNC({col}, 'WW')",
        "P1M": "TRUNC({col}, 'MONTH')",
        "P0.25Y": "TRUNC({col}, 'Q')",
        "P1Y": "TRUNC({col}, 'YYYY')",
    }

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "from_unixtime({col})"

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.DATE:
            return f"CAST('{dttm.date().isoformat()}' AS DATE)"
        if tt == utils.TemporalType.TIMESTAMP:
            return f"""CAST('{dttm.isoformat(timespec="microseconds")}' AS TIMESTAMP)"""
        return None

    @classmethod
    def get_schema_names(cls, inspector: Inspector) -> List[str]:
        schemas = [
            row[0]
            for row in inspector.engine.execute("SHOW SCHEMAS")
            if not row[0].startswith("_")
        ]
        return schemas
