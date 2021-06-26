import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User

from rabbitai.annotation_layers.commands.exceptions import (
    AnnotationLayerDeleteFailedError,
    AnnotationLayerDeleteIntegrityError,
    AnnotationLayerNotFoundError,
)
from rabbitai.annotation_layers.dao import AnnotationLayerDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.annotations import AnnotationLayer

logger = logging.getLogger(__name__)


class DeleteAnnotationLayerCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[AnnotationLayer] = None

    def run(self) -> Model:
        self.validate()
        try:
            annotation_layer = AnnotationLayerDAO.delete(self._model)
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationLayerDeleteFailedError()
        return annotation_layer

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = AnnotationLayerDAO.find_by_id(self._model_id)
        if not self._model:
            raise AnnotationLayerNotFoundError()
        if AnnotationLayerDAO.has_annotations(self._model.id):
            raise AnnotationLayerDeleteIntegrityError()
