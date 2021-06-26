from typing import List
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from freezegun.api import FakeDatetime  # type: ignore

from rabbitai.extensions import db
from rabbitai.models.reports import ReportScheduleType
from rabbitai.tasks.scheduler import cron_schedule_window, scheduler
from tests.reports.utils import insert_report_schedule
from tests.test_app import app


@pytest.mark.parametrize(
    "current_dttm, cron, excepted",
    [
        ("2020-01-01T08:59:01Z", "0 9 * * *", []),
        ("2020-01-01T08:59:02Z", "0 9 * * *", [FakeDatetime(2020, 1, 1, 9, 0)]),
        ("2020-01-01T08:59:59Z", "0 9 * * *", [FakeDatetime(2020, 1, 1, 9, 0)]),
        ("2020-01-01T09:00:00Z", "0 9 * * *", [FakeDatetime(2020, 1, 1, 9, 0)]),
        ("2020-01-01T09:00:01Z", "0 9 * * *", []),
    ],
)
def test_cron_schedule_window(
    current_dttm: str, cron: str, excepted: List[FakeDatetime]
):
    """
    Reports scheduler: Test cron schedule window
    """
    with app.app_context():

        with freeze_time(current_dttm):
            datetimes = cron_schedule_window(cron)
            assert list(datetimes) == excepted


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_timeout(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():

        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT, name=f"report", crontab=f"0 9 * * *",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            assert execute_mock.call_args[1]["soft_time_limit"] == 3601
            assert execute_mock.call_args[1]["time_limit"] == 3610
        db.session.delete(report_schedule)
        db.session.commit()


@patch("rabbitai.tasks.scheduler.execute.apply_async")
def test_scheduler_celery_no_timeout(execute_mock):
    """
    Reports scheduler: Test scheduler setting celery soft and hard timeout
    """
    with app.app_context():
        app.config["ALERT_REPORTS_WORKING_TIME_OUT_KILL"] = False
        report_schedule = insert_report_schedule(
            type=ReportScheduleType.ALERT, name=f"report", crontab=f"0 9 * * *",
        )

        with freeze_time("2020-01-01T09:00:00Z"):
            scheduler()
            assert execute_mock.call_args[1] == {"eta": FakeDatetime(2020, 1, 1, 9, 0)}
        db.session.delete(report_schedule)
        db.session.commit()
