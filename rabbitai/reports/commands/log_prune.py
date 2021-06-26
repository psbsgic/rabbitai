import logging
from datetime import datetime, timedelta

from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.reports import ReportSchedule
from rabbitai.reports.commands.exceptions import ReportSchedulePruneLogError
from rabbitai.reports.dao import ReportScheduleDAO
from rabbitai.utils.celery import session_scope

logger = logging.getLogger(__name__)


class AsyncPruneReportScheduleLogCommand(BaseCommand):
    """
    Prunes logs from all report schedules
    """

    def __init__(self, worker_context: bool = True):
        self._worker_context = worker_context

    def run(self) -> None:
        with session_scope(nullpool=True) as session:
            self.validate()
            prune_errors = []

            for report_schedule in session.query(ReportSchedule).all():
                if report_schedule.log_retention is not None:
                    from_date = datetime.utcnow() - timedelta(
                        days=report_schedule.log_retention
                    )
                    try:
                        row_count = ReportScheduleDAO.bulk_delete_logs(
                            report_schedule, from_date, session=session, commit=False
                        )
                        logger.info(
                            "Deleted %s logs for report schedule id: %s",
                            str(row_count),
                            str(report_schedule.id),
                        )
                    except DAODeleteFailedError as ex:
                        prune_errors.append(str(ex))
            if prune_errors:
                raise ReportSchedulePruneLogError(";".join(prune_errors))

    def validate(self) -> None:
        pass
