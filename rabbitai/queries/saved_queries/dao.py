import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from rabbitai.dao.base import BaseDAO
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.extensions import db
from rabbitai.models.sql_lab import SavedQuery
from rabbitai.queries.saved_queries.filters import SavedQueryFilter

logger = logging.getLogger(__name__)


class SavedQueryDAO(BaseDAO):
    model_cls = SavedQuery
    base_filter = SavedQueryFilter

    @staticmethod
    def bulk_delete(models: Optional[List[SavedQuery]], commit: bool = True) -> None:
        item_ids = [model.id for model in models] if models else []
        try:
            db.session.query(SavedQuery).filter(SavedQuery.id.in_(item_ids)).delete(
                synchronize_session="fetch"
            )
            if commit:
                db.session.commit()
        except SQLAlchemyError:
            if commit:
                db.session.rollback()
            raise DAODeleteFailedError()
