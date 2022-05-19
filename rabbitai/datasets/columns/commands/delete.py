import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.connectors.sqla.models import TableColumn
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.datasets.columns.commands.exceptions import (
    DatasetColumnDeleteFailedError,
    DatasetColumnForbiddenError,
    DatasetColumnNotFoundError,
)
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class DeleteDatasetColumnCommand(BaseCommand):
    """删除数据集列命令。"""

    def __init__(self, user: User, dataset_id: int, model_id: int):
        self._actor = user
        self._dataset_id = dataset_id
        self._model_id = model_id
        self._model: Optional[TableColumn] = None

    def run(self) -> Model:
        self.validate()
        try:
            if not self._model:
                raise DatasetColumnNotFoundError()
            column = DatasetDAO.delete_column(self._model)
            return column
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise DatasetColumnDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = DatasetDAO.find_dataset_column(self._dataset_id, self._model_id)
        if not self._model:
            raise DatasetColumnNotFoundError()
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise DatasetColumnForbiddenError()
