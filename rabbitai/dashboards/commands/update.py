import logging
from typing import Any, Dict, List, Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.commands.base import BaseCommand
from rabbitai.commands.utils import populate_owners, populate_roles
from rabbitai.dao.exceptions import DAOUpdateFailedError
from rabbitai.dashboards.commands.exceptions import (
    DashboardForbiddenError,
    DashboardInvalidError,
    DashboardNotFoundError,
    DashboardSlugExistsValidationError,
    DashboardUpdateFailedError,
)
from rabbitai.dashboards.dao import DashboardDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.models.dashboard import Dashboard
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class UpdateDashboardCommand(BaseCommand):
    def __init__(self, user: User, model_id: int, data: Dict[str, Any]):
        self._actor = user
        self._model_id = model_id
        self._properties = data.copy()
        self._model: Optional[Dashboard] = None

    def run(self) -> Model:
        self.validate()
        try:
            dashboard = DashboardDAO.update(self._model, self._properties, commit=False)
            dashboard = DashboardDAO.update_charts_owners(dashboard, commit=True)
        except DAOUpdateFailedError as ex:
            logger.exception(ex.exception)
            raise DashboardUpdateFailedError()
        return dashboard

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        owners_ids: Optional[List[int]] = self._properties.get("owners")
        roles_ids: Optional[List[int]] = self._properties.get("roles")
        slug: Optional[str] = self._properties.get("slug")

        # Validate/populate model exists
        self._model = DashboardDAO.find_by_id(self._model_id)
        if not self._model:
            raise DashboardNotFoundError()
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise DashboardForbiddenError()

        # Validate slug uniqueness
        if not DashboardDAO.validate_update_slug_uniqueness(self._model_id, slug):
            exceptions.append(DashboardSlugExistsValidationError())

        # Validate/Populate owner
        if owners_ids is None:
            owners_ids = [owner.id for owner in self._model.owners]
        try:
            owners = populate_owners(self._actor, owners_ids)
            self._properties["owners"] = owners
        except ValidationError as ex:
            exceptions.append(ex)
        if exceptions:
            exception = DashboardInvalidError()
            exception.add_list(exceptions)
            raise exception

        # Validate/Populate role
        if roles_ids is None:
            roles_ids = [role.id for role in self._model.roles]
        try:
            roles = populate_roles(roles_ids)
            self._properties["roles"] = roles
        except ValidationError as ex:
            exceptions.append(ex)
        if exceptions:
            exception = DashboardInvalidError()
            exception.add_list(exceptions)
            raise exception
