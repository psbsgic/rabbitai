import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from flask_babel import lazy_gettext as _

from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.databases.commands.exceptions import (
    DatabaseDeleteDatasetsExistFailedError,
    DatabaseDeleteFailedError,
    DatabaseDeleteFailedReportsExistError,
    DatabaseNotFoundError,
)
from rabbitai.databases.dao import DatabaseDAO
from rabbitai.models.core import Database
from rabbitai.reports.dao import ReportScheduleDAO

logger = logging.getLogger(__name__)


class DeleteDatabaseCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[Database] = None

    def run(self) -> Model:
        self.validate()
        try:
            database = DatabaseDAO.delete(self._model)
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise DatabaseDeleteFailedError()
        return database

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = DatabaseDAO.find_by_id(self._model_id)
        if not self._model:
            raise DatabaseNotFoundError()
        # Check there are no associated ReportSchedules
        reports = ReportScheduleDAO.find_by_database_id(self._model_id)

        if reports:
            report_names = [report.name for report in reports]
            raise DatabaseDeleteFailedReportsExistError(
                _("There are associated alerts or reports: %s" % ",".join(report_names))
            )
        # Check if there are datasets for this database
        if self._model.tables:
            raise DatabaseDeleteDatasetsExistFailedError()
