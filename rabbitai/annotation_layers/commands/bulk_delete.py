import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.annotation_layers.commands.exceptions import (
    AnnotationLayerBulkDeleteFailedError,
    AnnotationLayerBulkDeleteIntegrityError,
    AnnotationLayerNotFoundError,
)
from rabbitai.annotation_layers.dao import AnnotationLayerDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.annotations import AnnotationLayer

logger = logging.getLogger(__name__)


class BulkDeleteAnnotationLayerCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[AnnotationLayer]] = None

    def run(self) -> None:
        self.validate()
        try:
            AnnotationLayerDAO.bulk_delete(self._models)
            return None
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationLayerBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = AnnotationLayerDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise AnnotationLayerNotFoundError()
        if AnnotationLayerDAO.has_annotations(self._model_ids):
            raise AnnotationLayerBulkDeleteIntegrityError()
