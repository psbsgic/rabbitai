# pylint: disable=unused-argument, invalid-name

from datetime import datetime
from typing import List

import pytest
import pytz
from dateutil import parser
from flask.ctx import AppContext
from freezegun import freeze_time
from freezegun.api import FakeDatetime  # type: ignore

from rabbitai.tasks.cron_util import cron_schedule_window


@pytest.mark.parametrize(
    "current_dttm, cron, expected",
    [
        ("2020-01-01T08:59:01Z", "0 1 * * *", []),
        (
            "2020-01-01T08:59:02Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 9, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T08:59:59Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 9, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T09:00:00Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 9, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        ("2020-01-01T09:00:01Z", "0 1 * * *", []),
    ],
)
def test_cron_schedule_window_los_angeles(
    app_context: AppContext, current_dttm: str, cron: str, expected: List[FakeDatetime]
) -> None:
    """
    Reports scheduler: Test cron schedule window for "America/Los_Angeles"
    """

    with freeze_time(current_dttm):
        datetimes = cron_schedule_window(cron, "America/Los_Angeles")
        assert (
            list(cron.strftime("%A, %d %B %Y, %H:%M:%S") for cron in datetimes)
            == expected
        )


@pytest.mark.parametrize(
    "current_dttm, cron, expected",
    [
        ("2020-01-01T05:59:01Z", "0 1 * * *", []),
        (
            "2020-01-01T05:59:02Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T5:59:59Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T6:00:00",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        ("2020-01-01T6:00:01Z", "0 1 * * *", []),
    ],
)
def test_cron_schedule_window_new_york(
    app_context: AppContext, current_dttm: str, cron: str, expected: List[FakeDatetime]
) -> None:
    """
    Reports scheduler: Test cron schedule window for "America/New_York"
    """

    with freeze_time(current_dttm, tz_offset=0):
        datetimes = cron_schedule_window(cron, "America/New_York")
        assert (
            list(cron.strftime("%A, %d %B %Y, %H:%M:%S") for cron in datetimes)
            == expected
        )


@pytest.mark.parametrize(
    "current_dttm, cron, expected",
    [
        ("2020-01-01T06:59:01Z", "0 1 * * *", []),
        (
            "2020-01-01T06:59:02Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 7, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T06:59:59Z",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 7, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-01-01T07:00:00",
            "0 1 * * *",
            [FakeDatetime(2020, 1, 1, 7, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        ("2020-01-01T07:00:01Z", "0 1 * * *", []),
    ],
)
def test_cron_schedule_window_chicago(
    app_context: AppContext, current_dttm: str, cron: str, expected: List[FakeDatetime]
) -> None:
    """
    Reports scheduler: Test cron schedule window for "America/Chicago"
    """

    with freeze_time(current_dttm, tz_offset=0):
        datetimes = cron_schedule_window(cron, "America/Chicago")
        assert (
            list(cron.strftime("%A, %d %B %Y, %H:%M:%S") for cron in datetimes)
            == expected
        )


@pytest.mark.parametrize(
    "current_dttm, cron, expected",
    [
        ("2020-07-01T05:59:01Z", "0 1 * * *", []),
        (
            "2020-07-01T05:59:02Z",
            "0 1 * * *",
            [FakeDatetime(2020, 7, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-07-01T05:59:59Z",
            "0 1 * * *",
            [FakeDatetime(2020, 7, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        (
            "2020-07-01T06:00:00",
            "0 1 * * *",
            [FakeDatetime(2020, 7, 1, 6, 0).strftime("%A, %d %B %Y, %H:%M:%S")],
        ),
        ("2020-07-01T06:00:01Z", "0 1 * * *", []),
    ],
)
def test_cron_schedule_window_chicago_daylight(
    app_context: AppContext, current_dttm: str, cron: str, expected: List[FakeDatetime]
) -> None:
    """
    Reports scheduler: Test cron schedule window for "America/Chicago"
    """

    with freeze_time(current_dttm, tz_offset=0):
        datetimes = cron_schedule_window(cron, "America/Chicago")
        assert (
            list(cron.strftime("%A, %d %B %Y, %H:%M:%S") for cron in datetimes)
            == expected
        )
