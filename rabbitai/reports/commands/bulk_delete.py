import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.models.reports import ReportSchedule
from rabbitai.reports.commands.exceptions import (
    ReportScheduleBulkDeleteFailedError,
    ReportScheduleForbiddenError,
    ReportScheduleNotFoundError,
)
from rabbitai.reports.dao import ReportScheduleDAO
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class BulkDeleteReportScheduleCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[ReportSchedule]] = None

    def run(self) -> None:
        self.validate()
        try:
            ReportScheduleDAO.bulk_delete(self._models)
            return None
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise ReportScheduleBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = ReportScheduleDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise ReportScheduleNotFoundError()

        # Check ownership
        for model in self._models:
            try:
                check_ownership(model)
            except RabbitaiSecurityException:
                raise ReportScheduleForbiddenError()
