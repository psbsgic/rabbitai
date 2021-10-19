# -*- coding: utf-8 -*-

from sqlalchemy.dialects import registry

from rabbitai.db_engine_specs.impala import ImpalaEngineSpec


class AscendEngineSpec(ImpalaEngineSpec):
    """Engine spec for Ascend.io (Hive2+TLS) using Cloudera's Impala"""

    engine = "ascend"
    registry.register("ascend", "impala.sqlalchemy", "ImpalaDialect")

    engine_name = "Ascend"

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
