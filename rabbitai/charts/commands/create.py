import logging
from typing import Any, Dict, List, Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.charts.commands.exceptions import (
    ChartCreateFailedError,
    ChartInvalidError,
    DashboardsNotFoundValidationError,
)
from rabbitai.charts.dao import ChartDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.commands.utils import get_datasource_by_id, populate_owners
from rabbitai.dao.exceptions import DAOCreateFailedError
from rabbitai.dashboards.dao import DashboardDAO

logger = logging.getLogger(__name__)


class CreateChartCommand(BaseCommand):
    def __init__(self, user: User, data: Dict[str, Any]):
        self._actor = user
        self._properties = data.copy()

    def run(self) -> Model:
        self.validate()
        try:
            chart = ChartDAO.create(self._properties)
        except DAOCreateFailedError as ex:
            logger.exception(ex.exception)
            raise ChartCreateFailedError()
        return chart

    def validate(self) -> None:
        exceptions = list()
        datasource_type = self._properties["datasource_type"]
        datasource_id = self._properties["datasource_id"]
        dashboard_ids = self._properties.get("dashboards", [])
        owner_ids: Optional[List[int]] = self._properties.get("owners")

        # Validate/Populate datasource
        try:
            datasource = get_datasource_by_id(datasource_id, datasource_type)
            self._properties["datasource_name"] = datasource.name
        except ValidationError as ex:
            exceptions.append(ex)

        # Validate/Populate dashboards
        dashboards = DashboardDAO.find_by_ids(dashboard_ids)
        if len(dashboards) != len(dashboard_ids):
            exceptions.append(DashboardsNotFoundValidationError())
        self._properties["dashboards"] = dashboards

        try:
            owners = populate_owners(self._actor, owner_ids)
            self._properties["owners"] = owners
        except ValidationError as ex:
            exceptions.append(ex)
        if exceptions:
            exception = ChartInvalidError()
            exception.add_list(exceptions)
            raise exception
