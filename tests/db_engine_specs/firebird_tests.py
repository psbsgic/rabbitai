from datetime import datetime
from unittest import mock

import pytest

from rabbitai.db_engine_specs.firebird import FirebirdEngineSpec

grain_expressions = {
    None: "timestamp_column",
    "PT1S": (
        "CAST(CAST(timestamp_column AS DATE) "
        "|| ' ' "
        "|| EXTRACT(HOUR FROM timestamp_column) "
        "|| ':' "
        "|| EXTRACT(MINUTE FROM timestamp_column) "
        "|| ':' "
        "|| FLOOR(EXTRACT(SECOND FROM timestamp_column)) AS TIMESTAMP)"
    ),
    "PT1M": (
        "CAST(CAST(timestamp_column AS DATE) "
        "|| ' ' "
        "|| EXTRACT(HOUR FROM timestamp_column) "
        "|| ':' "
        "|| EXTRACT(MINUTE FROM timestamp_column) "
        "|| ':00' AS TIMESTAMP)"
    ),
    "P1D": "CAST(timestamp_column AS DATE)",
    "P1M": (
        "CAST(EXTRACT(YEAR FROM timestamp_column) "
        "|| '-' "
        "|| EXTRACT(MONTH FROM timestamp_column) "
        "|| '-01' AS DATE)"
    ),
    "P1Y": "CAST(EXTRACT(YEAR FROM timestamp_column) || '-01-01' AS DATE)",
}


@pytest.mark.parametrize("grain,expected", grain_expressions.items())
def test_time_grain_expressions(grain, expected):
    assert (
        FirebirdEngineSpec._time_grain_expressions[grain].format(col="timestamp_column")
        == expected
    )


def test_epoch_to_dttm():
    assert (
        FirebirdEngineSpec.epoch_to_dttm().format(col="timestamp_column")
        == "DATEADD(second, timestamp_column, CAST('00:00:00' AS TIMESTAMP))"
    )


def test_convert_dttm():
    dttm = datetime(2021, 1, 1)
    assert (
        FirebirdEngineSpec.convert_dttm("timestamp", dttm)
        == "CAST('2021-01-01 00:00:00' AS TIMESTAMP)"
    )
    assert (
        FirebirdEngineSpec.convert_dttm("TIMESTAMP", dttm)
        == "CAST('2021-01-01 00:00:00' AS TIMESTAMP)"
    )
    assert FirebirdEngineSpec.convert_dttm("TIME", dttm) == "CAST('00:00:00' AS TIME)"
    assert FirebirdEngineSpec.convert_dttm("DATE", dttm) == "CAST('2021-01-01' AS DATE)"
    assert FirebirdEngineSpec.convert_dttm("STRING", dttm) is None
