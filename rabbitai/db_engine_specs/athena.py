# -*- coding: utf-8 -*-

import re
from datetime import datetime
from typing import Any, Dict, Optional, Pattern, Tuple

from flask_babel import gettext as __

from rabbitai.db_engine_specs.base import BaseEngineSpec
from rabbitai.errors import RabbitaiErrorType
from rabbitai.utils import core as utils

SYNTAX_ERROR_REGEX = re.compile(
    ": mismatched input '(?P<syntax_error>.*?)'. Expecting: "
)


class AthenaEngineSpec(BaseEngineSpec):
    engine = "awsathena"
    engine_name = "Amazon Athena"

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "date_trunc('second', CAST({col} AS TIMESTAMP))",
        "PT1M": "date_trunc('minute', CAST({col} AS TIMESTAMP))",
        "PT1H": "date_trunc('hour', CAST({col} AS TIMESTAMP))",
        "P1D": "date_trunc('day', CAST({col} AS TIMESTAMP))",
        "P1W": "date_trunc('week', CAST({col} AS TIMESTAMP))",
        "P1M": "date_trunc('month', CAST({col} AS TIMESTAMP))",
        "P0.25Y": "date_trunc('quarter', CAST({col} AS TIMESTAMP))",
        "P1Y": "date_trunc('year', CAST({col} AS TIMESTAMP))",
        "P1W/1970-01-03T00:00:00Z": "date_add('day', 5, date_trunc('week', \
                                    date_add('day', 1, CAST({col} AS TIMESTAMP))))",
        "1969-12-28T00:00:00Z/P1W": "date_add('day', -1, date_trunc('week', \
                                    date_add('day', 1, CAST({col} AS TIMESTAMP))))",
    }
    """时间刻度表达式字典。"""

    custom_errors: Dict[Pattern[str], Tuple[str, RabbitaiErrorType, Dict[str, Any]]] = {
        SYNTAX_ERROR_REGEX: (
            __(
                "Please check your query for syntax errors at or "
                'near "%(syntax_error)s". Then, try running your query again.'
            ),
            RabbitaiErrorType.SYNTAX_ERROR,
            {},
        ),
    }

    @classmethod
    def convert_dttm(cls, target_type: str, dttm: datetime) -> Optional[str]:
        """
        转换指定日期时间。

        :param target_type: 目标类型名称。
        :param dttm: 日期时间对象。
        :return:
        """

        tt = target_type.upper()
        if tt == utils.TemporalType.DATE:
            return f"from_iso8601_date('{dttm.date().isoformat()}')"
        if tt == utils.TemporalType.TIMESTAMP:
            datetime_formatted = dttm.isoformat(timespec="microseconds")
            return f"""from_iso8601_timestamp('{datetime_formatted}')"""
        return None

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "from_unixtime({col})"

    @staticmethod
    def _mutate_label(label: str) -> str:
        """
        Athena only supports lowercase column names and aliases.

        :param label: Expected expression label
        :return: Conditionally mutated label
        """
        return label.lower()
