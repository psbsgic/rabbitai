import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User

from rabbitai.annotation_layers.annotations.commands.exceptions import (
    AnnotationDeleteFailedError,
    AnnotationNotFoundError,
)
from rabbitai.annotation_layers.annotations.dao import AnnotationDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.annotations import Annotation

logger = logging.getLogger(__name__)


class DeleteAnnotationCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[Annotation] = None

    def run(self) -> Model:
        self.validate()
        try:
            annotation = AnnotationDAO.delete(self._model)
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationDeleteFailedError()
        return annotation

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = AnnotationDAO.find_by_id(self._model_id)
        if not self._model:
            raise AnnotationNotFoundError()
