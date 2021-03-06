import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.annotation_layers.annotations.commands.exceptions import (
    AnnotationDatesValidationError,
    AnnotationInvalidError,
    AnnotationNotFoundError,
    AnnotationUniquenessValidationError,
    AnnotationUpdateFailedError,
)
from rabbitai.annotation_layers.annotations.dao import AnnotationDAO
from rabbitai.annotation_layers.commands.exceptions import AnnotationLayerNotFoundError
from rabbitai.annotation_layers.dao import AnnotationLayerDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAOUpdateFailedError
from rabbitai.models.annotations import Annotation

logger = logging.getLogger(__name__)


class UpdateAnnotationCommand(BaseCommand):
    def __init__(self, user: User, model_id: int, data: Dict[str, Any]):
        self._actor = user
        self._model_id = model_id
        self._properties = data.copy()
        self._model: Optional[Annotation] = None

    def run(self) -> Model:
        self.validate()
        try:
            annotation = AnnotationDAO.update(self._model, self._properties)
        except DAOUpdateFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationUpdateFailedError()
        return annotation

    def validate(self) -> None:
        exceptions: List[ValidationError] = list()
        layer_id: Optional[int] = self._properties.get("layer")
        short_descr: str = self._properties.get("short_descr", "")

        # Validate/populate model exists
        self._model = AnnotationDAO.find_by_id(self._model_id)
        if not self._model:
            raise AnnotationNotFoundError()
        # Validate/populate layer exists
        if layer_id:
            annotation_layer = AnnotationLayerDAO.find_by_id(layer_id)
            if not annotation_layer:
                raise AnnotationLayerNotFoundError()
            self._properties["layer"] = annotation_layer

            # Validate short descr uniqueness on this layer
            if not AnnotationDAO.validate_update_uniqueness(
                layer_id, short_descr, annotation_id=self._model_id,
            ):
                exceptions.append(AnnotationUniquenessValidationError())
        else:
            self._properties["layer"] = self._model.layer

        # validate date time sanity
        start_dttm: Optional[datetime] = self._properties.get("start_dttm")
        end_dttm: Optional[datetime] = self._properties.get("end_dttm")

        if start_dttm and end_dttm and end_dttm < start_dttm:
            exceptions.append(AnnotationDatesValidationError())

        if exceptions:
            exception = AnnotationInvalidError()
            exception.add_list(exceptions)
            raise exception
