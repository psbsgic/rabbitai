import logging
from typing import List, Optional

from flask_appbuilder.security.sqla.models import User

from rabbitai.commands.base import BaseCommand
from rabbitai.commands.exceptions import DeleteFailedError
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.datasets.commands.exceptions import (
    DatasetBulkDeleteFailedError,
    DatasetForbiddenError,
    DatasetNotFoundError,
)
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.extensions import db, security_manager
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class BulkDeleteDatasetCommand(BaseCommand):
    def __init__(self, user: User, model_ids: List[int]):
        self._actor = user
        self._model_ids = model_ids
        self._models: Optional[List[SqlaTable]] = None

    def run(self) -> None:
        self.validate()
        if not self._models:
            return None
        try:
            DatasetDAO.bulk_delete(self._models)
            for model in self._models:
                view_menu = (
                    security_manager.find_view_menu(model.get_perm()) if model else None
                )

                if view_menu:
                    permission_views = (
                        db.session.query(security_manager.permissionview_model)
                        .filter_by(view_menu=view_menu)
                        .all()
                    )

                    for permission_view in permission_views:
                        db.session.delete(permission_view)
                    if view_menu:
                        db.session.delete(view_menu)
                else:
                    if not view_menu:
                        logger.error(
                            "Could not find the data access permission for the dataset",
                            exc_info=True,
                        )
            db.session.commit()

            return None
        except DeleteFailedError as ex:
            logger.exception(ex.exception)
            raise DatasetBulkDeleteFailedError()

    def validate(self) -> None:
        # Validate/populate model exists
        self._models = DatasetDAO.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise DatasetNotFoundError()
        # Check ownership
        for model in self._models:
            try:
                check_ownership(model)
            except RabbitaiSecurityException:
                raise DatasetForbiddenError()
