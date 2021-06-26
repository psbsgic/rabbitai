import logging
from typing import Optional

from flask_appbuilder.models.sqla import Model
from flask_appbuilder.security.sqla.models import User
from sqlalchemy.exc import SQLAlchemyError

from rabbitai.commands.base import BaseCommand
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.datasets.commands.exceptions import (
    DatasetDeleteFailedError,
    DatasetForbiddenError,
    DatasetNotFoundError,
)
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.extensions import db, security_manager
from rabbitai.views.base import check_ownership

logger = logging.getLogger(__name__)


class DeleteDatasetCommand(BaseCommand):
    def __init__(self, user: User, model_id: int):
        self._actor = user
        self._model_id = model_id
        self._model: Optional[SqlaTable] = None

    def run(self) -> Model:
        self.validate()
        try:
            dataset = DatasetDAO.delete(self._model, commit=False)

            view_menu = (
                security_manager.find_view_menu(self._model.get_perm())
                if self._model
                else None
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
        except (SQLAlchemyError, DAODeleteFailedError) as ex:
            logger.exception(ex)
            db.session.rollback()
            raise DatasetDeleteFailedError()
        return dataset

    def validate(self) -> None:
        # Validate/populate model exists
        self._model = DatasetDAO.find_by_id(self._model_id)
        if not self._model:
            raise DatasetNotFoundError()
        # Check ownership
        try:
            check_ownership(self._model)
        except RabbitaiSecurityException:
            raise DatasetForbiddenError()
