import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.css_templates.commands.exceptions import (
    CssTemplateBulkDeleteFailedError,
    CssTemplateNotFoundError,
)
from rabbitai.css_templates.dao import CssTemplateDAO
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.models.core import CssTemplate

logger = logging.getLogger(__name__)


class BulkDeleteCssTemplateCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[CssTemplate]] = None

    def run(self) -> None:
        self.validate()
        try:
            CssTemplateDAO.bulk_delete(self._models)
            return None
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise CssTemplateBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = CssTemplateDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise CssTemplateNotFoundError()
