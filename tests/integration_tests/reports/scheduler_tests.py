from typing import List
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from freezegun.api import FakeDatetime  # type: ignore

from rabbitai.extensions import db
from rabbitai.models.reports import ReportScheduleType
from rabbitai.tasks.scheduler import scheduler
from tests.integration_tests.reports.utils import insert_report_schedule
from tests.integration_tests.test_app import app


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_timeout_ny(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():

        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT,
            name="report",
            crontab="0 4 * * *",
            timezone="America/New_York",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            assert execute_mock.call_args[1]["soft_time_limit"] == 3601
            assert execute_mock.call_args[1]["time_limit"] == 3610
        db.session.delete(report_schedule)
        db.session.commit()


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_no_timeout_ny(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():
        app.config["ALERT_REPORTS_WORKING_TIME_OUT_KILL"] = False
        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT,
            name="report",
            crontab="0 4 * * *",
            timezone="America/New_York",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            assert execute_mock.call_args[1] == {"eta": FakeDatetime(2020, 1, 1, 9, 0)}
        db.session.delete(report_schedule)
        db.session.commit()
        app.config["ALERT_REPORTS_WORKING_TIME_OUT_KILL"] = True


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_timeout_utc(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():

        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT,
            name="report",
            crontab="0 9 * * *",
            timezone="UTC",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            print(execute_mock.call_args)
            assert execute_mock.call_args[1]["soft_time_limit"] == 3601
            assert execute_mock.call_args[1]["time_limit"] == 3610
        db.session.delete(report_schedule)
        db.session.commit()


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_no_timeout_utc(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():
        app.config["ALERT_REPORTS_WORKING_TIME_OUT_KILL"] = False
        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT,
            name="report",
            crontab="0 9 * * *",
            timezone="UTC",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            assert execute_mock.call_args[1] == {"eta": FakeDatetime(2020, 1, 1, 9, 0)}
        db.session.delete(report_schedule)
        db.session.commit()
        app.config["ALERT_REPORTS_WORKING_TIME_OUT_KILL"] = True
