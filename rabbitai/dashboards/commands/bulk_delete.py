import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User
from flask_babel import lazy_gettext as _

from rabbitai.commands.base import BaseCommand
from rabbitai.commands.exceptions import DeleteFailedError
from rabbitai.dashboards.commands.exceptions import (
    DashboardBulkDeleteFailedError,
    DashboardBulkDeleteFailedReportsExistError,
    DashboardForbiddenError,
    DashboardNotFoundError,
)
from rabbitai.dashboards.dao import DashboardDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.models.dashboard import Dashboard
from rabbitai.reports.dao import ReportScheduleDAO
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class BulkDeleteDashboardCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[Dashboard]] = None

    def run(self) -> None:
        self.validate()
        try:
            DashboardDAO.bulk_delete(self._models)
            return None
        except DeleteFailedError as ex:
            logger.exception(ex.exception)
            raise DashboardBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = DashboardDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise DashboardNotFoundError()
        # Check there are no associated ReportSchedules
        reports = ReportScheduleDAO.find_by_dashboard_ids(self._model_ids)
        if reports:
            report_names = [report.name for report in reports]
            raise DashboardBulkDeleteFailedReportsExistError(
                _("There are associated alerts or reports: %s" % ",".join(report_names))
            )
        # Check ownership
        for model in self._models:
            try:
                check_ownership(model)
            except RabbitaiSecurityException:
                raise DashboardForbiddenError()
