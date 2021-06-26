import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.dashboard import Dashboard
from rabbitai.queries.saved_queries.commands.exceptions import (
    SavedQueryBulkDeleteFailedError,
    SavedQueryNotFoundError,
)
from rabbitai.queries.saved_queries.dao import SavedQueryDAO

logger = logging.getLogger(__name__)


class BulkDeleteSavedQueryCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[Dashboard]] = None

    def run(self) -> None:
        self.validate()
        try:
            SavedQueryDAO.bulk_delete(self._models)
            return None
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise SavedQueryBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = SavedQueryDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise SavedQueryNotFoundError()
