import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from rabbitai.dao.base import BaseDAO
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.extensions import db
from rabbitai.models.core import CssTemplate

logger = logging.getLogger(__name__)


class CssTemplateDAO(BaseDAO):
    model_cls = CssTemplate

    @staticmethod
    def bulk_delete(models: Optional[List[CssTemplate]], commit: bool = True) -> None:
        item_ids = [model.id for model in models] if models else []
        try:
            db.session.query(CssTemplate).filter(CssTemplate.id.in_(item_ids)).delete(
                synchronize_session="fetch"
            )
            if commit:
                db.session.commit()
        except SQLAlchemyError:
            if commit:
                db.session.rollback()
            raise DAODeleteFailedError()
