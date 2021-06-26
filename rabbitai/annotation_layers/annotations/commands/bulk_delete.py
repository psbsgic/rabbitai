import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.annotation_layers.annotations.commands.exceptions import (
    AnnotationBulkDeleteFailedError,
    AnnotationNotFoundError,
)
from rabbitai.annotation_layers.annotations.dao import AnnotationDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.annotations import Annotation

logger = logging.getLogger(__name__)


class BulkDeleteAnnotationCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[Annotation]] = None

    def run(self) -> None:
        self.validate()
        try:
            AnnotationDAO.bulk_delete(self._models)
            return None
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = AnnotationDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise AnnotationNotFoundError()
