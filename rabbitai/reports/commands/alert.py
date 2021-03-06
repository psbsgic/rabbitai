import json
import logging
from operator import eq, ge, gt, le, lt, ne
from timeit import default_timer
from typing import Optional

import numpy as np
import pandas as pd
from celery.exceptions import SoftTimeLimitExceeded
from flask_babel import lazy_gettext as _

from rabbitai import jinja_context
from rabbitai.commands.base import BaseCommand
from rabbitai.models.reports import ReportSchedule, ReportScheduleValidatorType
from rabbitai.reports.commands.exceptions import (
    AlertQueryError,
    AlertQueryInvalidTypeError,
    AlertQueryMultipleColumnsError,
    AlertQueryMultipleRowsError,
    AlertQueryTimeout,
    AlertValidatorConfigError,
)

logger = logging.getLogger(__name__)


ALERT_SQL_LIMIT = 2
# All sql statements have an applied LIMIT,
# to avoid heavy loads done by a user mistake
OPERATOR_FUNCTIONS = {">=": ge, ">": gt, "<=": le, "<": lt, "==": eq, "!=": ne}


class AlertCommand(BaseCommand):
    def __init__(self, report_schedule: ReportSchedule):
        self._report_schedule = report_schedule
        self._result: Optional[float] = None

    def run(self) -> bool:
        """
        Executes an alert SQL query and validates it.
        Will set the report_schedule.last_value or last_value_row_json
        with the query result

        :return: bool, if the alert triggered or not
        :raises AlertQueryError: SQL query is not valid
        :raises AlertQueryInvalidTypeError: The output from the SQL query
        is not an allowed type
        :raises AlertQueryMultipleColumnsError: The SQL query returned multiple columns
        :raises AlertQueryMultipleRowsError: The SQL query returned multiple rows
        :raises AlertQueryTimeout: The SQL query received a celery soft timeout
        :raises AlertValidatorConfigError: The validator query data is not valid
        """
        self.validate()

        if self._is_validator_not_null:
            self._report_schedule.last_value_row_json = str(self._result)
            return self._result not in (0, None, np.nan)
        self._report_schedule.last_value = self._result
        try:
            operator = json.loads(self._report_schedule.validator_config_json)["op"]
            threshold = json.loads(self._report_schedule.validator_config_json)[
                "threshold"
            ]

            return OPERATOR_FUNCTIONS[operator](self._result, threshold)
        except (KeyError, json.JSONDecodeError):
            raise AlertValidatorConfigError()

    def _validate_not_null(self, rows: np.recarray) -> None:
        self._validate_result(rows)
        self._result = rows[0][1]

    @staticmethod
    def _validate_result(rows: np.recarray) -> None:
        # check if query return more then one row
        if len(rows) > 1:
            raise AlertQueryMultipleRowsError(
                message=_(
                    "Alert query returned more then one row. %s rows returned"
                    % len(rows),
                )
            )
        # check if query returned more then one column
        if len(rows[0]) > 2:
            raise AlertQueryMultipleColumnsError(
                # len is subtracted by 1 to discard pandas index column
                _(
                    "Alert query returned more then one column. %s columns returned"
                    % (len(rows[0]) - 1)
                )
            )

    def _validate_operator(self, rows: np.recarray) -> None:
        self._validate_result(rows)
        if rows[0][1] in (0, None, np.nan):
            self._result = 0.0
            return
        try:
            # Check if it's float or if we can convert it
            self._result = float(rows[0][1])
            return
        except (AssertionError, TypeError, ValueError):
            raise AlertQueryInvalidTypeError()

    @property
    def _is_validator_not_null(self) -> bool:
        return (
            self._report_schedule.validator_type == ReportScheduleValidatorType.NOT_NULL
        )

    @property
    def _is_validator_operator(self) -> bool:
        return (
            self._report_schedule.validator_type == ReportScheduleValidatorType.OPERATOR
        )

    def _execute_query(self) -> pd.DataFrame:
        """
        Executes the actual alert SQL query template

        :return: A pandas dataframe
        :raises AlertQueryError: SQL query is not valid
        :raises AlertQueryTimeout: The SQL query received a celery soft timeout
        """
        sql_template = jinja_context.get_template_processor(
            database=self._report_schedule.database
        )
        rendered_sql = sql_template.process_template(self._report_schedule.sql)
        try:
            limited_rendered_sql = self._report_schedule.database.apply_limit_to_sql(
                rendered_sql, ALERT_SQL_LIMIT
            )
            start = default_timer()
            df = self._report_schedule.database.get_df(limited_rendered_sql)
            stop = default_timer()
            logger.info(
                "Query for %s took %.2f ms",
                self._report_schedule.name,
                (stop - start) * 1000.0,
            )
            return df
        except SoftTimeLimitExceeded as ex:
            logger.warning("A timeout occurred while executing the alert query: %s", ex)
            raise AlertQueryTimeout()
        except Exception as ex:
            raise AlertQueryError(message=str(ex))

    def validate(self) -> None:
        """
        Validate the query result as a Pandas DataFrame
        """
        df = self._execute_query()

        if df.empty and self._is_validator_not_null:
            self._result = None
            return
        if df.empty and self._is_validator_operator:
            self._result = 0.0
            return
        rows = df.to_records()
        if self._is_validator_not_null:
            self._validate_not_null(rows)
            return
        self._validate_operator(rows)
