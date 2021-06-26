import json
import logging
from typing import Any, Dict, List, Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.commands.utils import populate_owners
from rabbitai.dao.exceptions import DAOCreateFailedError
from rabbitai.databases.dao import DatabaseDAO
from rabbitai.models.reports import ReportScheduleType
from rabbitai.reports.commands.base import BaseReportScheduleCommand
from rabbitai.reports.commands.exceptions import (
    DatabaseNotFoundValidationError,
    ReportScheduleAlertRequiredDatabaseValidationError,
    ReportScheduleCreateFailedError,
    ReportScheduleInvalidError,
    ReportScheduleNameUniquenessValidationError,
    ReportScheduleRequiredTypeValidationError,
)
from rabbitai.reports.dao import ReportScheduleDAO

logger = logging.getLogger(__name__)


class CreateReportScheduleCommand(BaseReportScheduleCommand):
    def __init__(self, user: User, data: Dict[str, Any]):
        self._actor = user
        self._properties = data.copy()

    def run(self) -> Model:
        self.validate()
        try:
            report_schedule = ReportScheduleDAO.create(self._properties)
        except DAOCreateFailedError as ex:
            logger.exception(ex.exception)
            raise ReportScheduleCreateFailedError()
        return report_schedule

    def validate(self) -> None:
        exceptions: List[ValidationError] = list()
        owner_ids: Optional[List[int]] = self._properties.get("owners")
        name = self._properties.get("name", "")
        report_type = self._properties.get("type")

        # Validate type is required
        if not report_type:
            exceptions.append(ReportScheduleRequiredTypeValidationError())

        # Validate name type uniqueness
        if report_type and not ReportScheduleDAO.validate_update_uniqueness(
            name, report_type
        ):
            exceptions.append(ReportScheduleNameUniquenessValidationError())

        # validate relation by report type
        if report_type == ReportScheduleType.ALERT:
            database_id = self._properties.get("database")
            if not database_id:
                exceptions.append(ReportScheduleAlertRequiredDatabaseValidationError())
            else:
                database = DatabaseDAO.find_by_id(database_id)
                if not database:
                    exceptions.append(DatabaseNotFoundValidationError())
                self._properties["database"] = database

        # Validate chart or dashboard relations
        self.validate_chart_dashboard(exceptions)

        if "validator_config_json" in self._properties:
            self._properties["validator_config_json"] = json.dumps(
                self._properties["validator_config_json"]
            )

        try:
            owners = populate_owners(self._actor, owner_ids)
            self._properties["owners"] = owners
        except ValidationError as ex:
            exceptions.append(ex)
        if exceptions:
            exception = ReportScheduleInvalidError()
            exception.add_list(exceptions)
            raise exception
