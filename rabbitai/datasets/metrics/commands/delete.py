import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.connectors.sqla.models import SqlMetric
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.datasets.metrics.commands.exceptions import (
    DatasetMetricDeleteFailedError,
    DatasetMetricForbiddenError,
    DatasetMetricNotFoundError,
)
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class DeleteDatasetMetricCommand(BaseCommand):
    def __init__(self, user: User, dataset_id: int, model_id: int):
        self._actor = user
        self._dataset_id = dataset_id
        self._model_id = model_id
        self._model: Optional[SqlMetric] = None

    def run(self) -> Model:
        self.validate()
        try:
            if not self._model:
                raise DatasetMetricNotFoundError()
            column = DatasetDAO.delete_metric(self._model)
            return column
        except DAODeleteFailedError as ex:
            logger.exception(ex.exception)
            raise DatasetMetricDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = DatasetDAO.find_dataset_metric(self._dataset_id, self._model_id)
        if not self._model:
            raise DatasetMetricNotFoundError()
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise DatasetMetricForbiddenError()
