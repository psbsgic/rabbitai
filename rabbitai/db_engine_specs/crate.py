# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.utils import core as utils

if TYPE_CHECKING:
    from rabbitai.connectors.sqla.models import TableColumn


class CrateEngineSpec(BaseEngineSpec):

    engine = "crate"
    engine_name = "CrateDB"

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
    def epoch_to_dttm(cls) -> str:
        return "{col} * 1000"

    @classmethod
    def epoch_ms_to_dttm(cls) -> str:
        return "{col}"

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.TIMESTAMP:
            return f"{dttm.timestamp() * 1000}"
        return None

    @classmethod
    def alter_new_orm_column(cls, orm_col: "TableColumn") -> None:
        if orm_col.type == "TIMESTAMP":
            orm_col.python_date_format = "epoch_ms"
