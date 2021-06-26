import logging
from typing import Any, Dict, List

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from marshmallow import ValidationError

from rabbitai.annotation_layers.commands.exceptions import (
    AnnotationLayerCreateFailedError,
    AnnotationLayerInvalidError,
    AnnotationLayerNameUniquenessValidationError,
)
from rabbitai.annotation_layers.dao import AnnotationLayerDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dao.exceptions import DAOCreateFailedError

logger = logging.getLogger(__name__)


class CreateAnnotationLayerCommand(BaseCommand):
    def __init__(self, user: User, data: Dict[str, Any]):
        self._actor = user
        self._properties = data.copy()

    def run(self) -> Model:
        self.validate()
        try:
            annotation_layer = AnnotationLayerDAO.create(self._properties)
        except DAOCreateFailedError as ex:
            logger.exception(ex.exception)
            raise AnnotationLayerCreateFailedError()
        return annotation_layer

    def validate(self) -> None:
        exceptions: List[ValidationError] = list()

        name = self._properties.get("name", "")

        if not AnnotationLayerDAO.validate_update_uniqueness(name):
            exceptions.append(AnnotationLayerNameUniquenessValidationError())

        if exceptions:
            exception = AnnotationLayerInvalidError()
            exception.add_list(exceptions)
            raise exception
