from datetime import datetime, timedelta, timezone as dt_timezone
from typing import Iterator

import pytz
from croniter import croniter

from rabbitai import app


def cron_schedule_window(cron: str, timezone: str) -> Iterator[datetime]:
    window_size = app.config["ALERT_REPORTS_CRON_WINDOW_SIZE"]
    # create a time-aware datetime in utc
    time_now = datetime.now(tz=dt_timezone.utc)
    tz = pytz.timezone(timezone)
    utc = pytz.timezone("UTC")
    # convert the current time to the user's local time for comparison
    time_now = time_now.astimezone(tz)
    start_at = time_now - timedelta(seconds=1)
    stop_at = time_now + timedelta(seconds=window_size)
    crons = croniter(cron, start_at)
    for schedule in crons.all_next(datetime):
        if schedule >= stop_at:
            break
        # convert schedule back to utc
        yield schedule.astimezone(utc).replace(tzinfo=None)
