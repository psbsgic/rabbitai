import logging
from typing import Any, Dict, List, Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.annotation_layers.commands.exceptions import (
    AnnotationLayerInvalidError,
    AnnotationLayerNameUniquenessValidationError,
    AnnotationLayerNotFoundError,
    AnnotationLayerUpdateFailedError,
)
from rabbitai.annotation_layers.dao import AnnotationLayerDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAOUpdateFailedError
from rabbitai.models.annotations import AnnotationLayer

logger = logging.getLogger(__name__)


class UpdateAnnotationLayerCommand(BaseCommand):
    def __init__(self, user: User, model_id: int, data: Dict[str, Any]):
        self._actor = user
        self._model_id = model_id
        self._properties = data.copy()
        self._model: Optional[AnnotationLayer] = None

    def run(self) -> Model:
        self.validate()
        try:
            annotation_layer = AnnotationLayerDAO.update(self._model, self._properties)
        except DAOUpdateFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationLayerUpdateFailedError()
        return annotation_layer

    def validate(self) -> None:
        exceptions: List[ValidationError] = list()
        name = self._properties.get("name", "")
        self._model = AnnotationLayerDAO.find_by_id(self._model_id)

        if not self._model:
            raise AnnotationLayerNotFoundError()

        if not AnnotationLayerDAO.validate_update_uniqueness(
            name, layer_id=self._model_id
        ):
            exceptions.append(AnnotationLayerNameUniquenessValidationError())

        if exceptions:
            exception = AnnotationLayerInvalidError()
            exception.add_list(exceptions)
            raise exception
