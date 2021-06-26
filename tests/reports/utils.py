from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai import db
from rabbitai.models.core import Database
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.reports import (
    ReportDataFormat,
    ReportExecutionLog,
    ReportRecipients,
    ReportSchedule,
    ReportState,
)
from rabbitai.models.slice import Slice


def insert_report_schedule(
    type: str,
    name: str,
    crontab: str,
    sql: Optional[str] = None,
    description: Optional[str] = None,
    chart: Optional[Slice] = None,
    dashboard: Optional[Dashboard] = None,
    database: Optional[Database] = None,
    owners: Optional[List[User]] = None,
    validator_type: Optional[str] = None,
    validator_config_json: Optional[str] = None,
    log_retention: Optional[int] = None,
    last_state: Optional[ReportState] = None,
    grace_period: Optional[int] = None,
    recipients: Optional[List[ReportRecipients]] = None,
    report_format: Optional[ReportDataFormat] = None,
    logs: Optional[List[ReportExecutionLog]] = None,
) -> ReportSchedule:
    owners = owners or []
    recipients = recipients or []
    logs = logs or []
    last_state = last_state or ReportState.NOOP
    report_schedule = ReportSchedule(
        type=type,
        name=name,
        crontab=crontab,
        sql=sql,
        description=description,
        chart=chart,
        dashboard=dashboard,
        database=database,
        owners=owners,
        validator_type=validator_type,
        validator_config_json=validator_config_json,
        log_retention=log_retention,
        grace_period=grace_period,
        recipients=recipients,
        logs=logs,
        last_state=last_state,
        report_format=report_format,
    )
    db.session.add(report_schedule)
    db.session.commit()
    return report_schedule
