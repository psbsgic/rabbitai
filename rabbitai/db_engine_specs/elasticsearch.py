from datetime import datetime
from typing import Dict, Optional, Type

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.db_engine_specs.exceptions import (
    RabbitaiDBAPIDatabaseError,
    RabbitaiDBAPIOperationalError,
    RabbitaiDBAPIProgrammingError,
)
from rabbitai.utils import core as utils


class ElasticSearchEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method
    engine = "elasticsearch"
    engine_name = "ElasticSearch (SQL API)"
    time_groupby_inline = True
    time_secondary_columns = True
    allows_joins = False
    allows_subqueries = True
    allows_sql_comments = False

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "HISTOGRAM({col}, INTERVAL 1 SECOND)",
        "PT1M": "HISTOGRAM({col}, INTERVAL 1 MINUTE)",
        "PT1H": "HISTOGRAM({col}, INTERVAL 1 HOUR)",
        "P1D": "HISTOGRAM({col}, INTERVAL 1 DAY)",
        "P1M": "HISTOGRAM({col}, INTERVAL 1 MONTH)",
        "P1Y": "HISTOGRAM({col}, INTERVAL 1 YEAR)",
    }

    type_code_map: Dict[int, str] = {}  # loaded from get_datatype only if needed

    @classmethod
    def get_dbapi_exception_mapping(cls) -> Dict[Type[Exception], Type[Exception]]:
        import es.exceptions as es_exceptions  # pylint: disable=import-error

        return {
            es_exceptions.DatabaseError: RabbitaiDBAPIDatabaseError,
            es_exceptions.OperationalError: RabbitaiDBAPIOperationalError,
            es_exceptions.ProgrammingError: RabbitaiDBAPIProgrammingError,
        }

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        if target_type.upper() == utils.TemporalType.DATETIME:
            return f"""CAST('{dttm.isoformat(timespec="seconds")}' AS DATETIME)"""
        return None


class OpenDistroEngineSpec(BaseEngineSpec):  # pylint: disable=abstract-method

    time_groupby_inline = True
    time_secondary_columns = True
    allows_joins = False
    allows_subqueries = True
    allows_sql_comments = False

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "date_format({col}, 'yyyy-MM-dd HH:mm:ss.000')",
        "PT1M": "date_format({col}, 'yyyy-MM-dd HH:mm:00.000')",
        "PT1H": "date_format({col}, 'yyyy-MM-dd HH:00:00.000')",
        "P1D": "date_format({col}, 'yyyy-MM-dd 00:00:00.000')",
        "P1M": "date_format({col}, 'yyyy-MM-01 00:00:00.000')",
        "P1Y": "date_format({col}, 'yyyy-01-01 00:00:00.000')",
    }

    engine = "odelasticsearch"
    engine_name = "ElasticSearch (OpenDistro SQL)"

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        if target_type.upper() == utils.TemporalType.DATETIME:
            return f"""'{dttm.isoformat(timespec="seconds")}'"""
        return None

    @staticmethod
    def _mutate_label(label: str) -> str:
        return label.replace(".", "_")
