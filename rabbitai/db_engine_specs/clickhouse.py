from datetime import datetime
from typing import Dict, Optional, Type

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.db_engine_specs.exceptions import RabbitaiDBAPIDatabaseError
from rabbitai.utils import core as utils


class ClickHouseEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    """Dialect for ClickHouse analytical DB."""

    engine = "clickhouse"
    engine_name = "ClickHouse"

    time_secondary_columns = True
    time_groupby_inline = True

    _time_grain_expressions = {
        None: "{col}",
        "PT1M": "toStartOfMinute(toDateTime({col}))",
        "PT5M": "toDateTime(intDiv(toUInt32(toDateTime({col})), 300)*300)",
        "PT10M": "toDateTime(intDiv(toUInt32(toDateTime({col})), 600)*600)",
        "PT15M": "toDateTime(intDiv(toUInt32(toDateTime({col})), 900)*900)",
        "PT0.5H": "toDateTime(intDiv(toUInt32(toDateTime({col})), 1800)*1800)",
        "PT1H": "toStartOfHour(toDateTime({col}))",
        "P1D": "toStartOfDay(toDateTime({col}))",
        "P1W": "toMonday(toDateTime({col}))",
        "P1M": "toStartOfMonth(toDateTime({col}))",
        "P0.25Y": "toStartOfQuarter(toDateTime({col}))",
        "P1Y": "toStartOfYear(toDateTime({col}))",
    }

    @classmethod
    def get_dbapi_exception_mapping(cls) -> Dict[Type[Exception], Type[Exception]]:
        from urllib3.exceptions import NewConnectionError

        return {NewConnectionError: RabbitaiDBAPIDatabaseError}

    @classmethod
    def get_dbapi_mapped_exception(cls, exception: Exception) -> Exception:
        new_exception = cls.get_dbapi_exception_mapping().get(type(exception))
        if new_exception == RabbitaiDBAPIDatabaseError:
            return RabbitaiDBAPIDatabaseError("Connection failed")
        if not new_exception:
            return exception
        return new_exception(str(exception))

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.DATE:
            return f"toDate('{dttm.date().isoformat()}')"
        if tt == utils.TemporalType.DATETIME:
            return f"""toDateTime('{dttm.isoformat(sep=" ", timespec="seconds")}')"""
        return None
