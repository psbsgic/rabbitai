import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from flask_babel import lazy_gettext as _

from rabbitai.charts.commands.exceptions import (
    ChartDeleteFailedError,
    ChartDeleteFailedReportsExistError,
    ChartForbiddenError,
    ChartNotFoundError,
)
from rabbitai.charts.dao import ChartDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice
from rabbitai.reports.dao import ReportScheduleDAO
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class DeleteChartCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[Slice] = None

    def run(self) -> Model:
        self.validate()
        try:
            Dashboard.clear_cache_for_slice(slice_id=self._model_id)
            chart = ChartDAO.delete(self._model)
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise ChartDeleteFailedError()
        return chart

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = ChartDAO.find_by_id(self._model_id)
        if not self._model:
            raise ChartNotFoundError()
        # Check there are no associated ReportSchedules
        reports = ReportScheduleDAO.find_by_chart_id(self._model_id)
        if reports:
            report_names = [report.name for report in reports]
            raise ChartDeleteFailedReportsExistError(
                _("There are associated alerts or reports: %s" % ",".join(report_names))
            )
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise ChartForbiddenError()
