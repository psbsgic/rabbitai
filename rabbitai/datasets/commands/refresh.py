import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.datasets.commands.exceptions import (
    DatasetForbiddenError,
    DatasetNotFoundError,
    DatasetRefreshFailedError,
)
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class RefreshDatasetCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[SqlaTable] = None

    def run(self) -> Model:
        self.validate()
        if self._model:
            try:
                self._model.fetch_metadata()
                return self._model
            except Exception as ex:
                logger.exception(ex)
                raise DatasetRefreshFailedError()
        raise DatasetRefreshFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = DatasetDAO.find_by_id(self._model_id)
        if not self._model:
            raise DatasetNotFoundError()
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise DatasetForbiddenError()
