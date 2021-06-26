import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from rabbitai.dao.base import BaseDAO
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.extensions import db
from rabbitai.models.annotations import Annotation

logger = logging.getLogger(__name__)


class AnnotationDAO(BaseDAO):
    model_cls = Annotation

    @staticmethod
    def bulk_delete(models: Optional[List[Annotation]], commit: bool = True) -> None:
        item_ids = [model.id for model in models] if models else []
        try:
            db.session.query(Annotation).filter(Annotation.id.in_(item_ids)).delete(
                synchronize_session="fetch"
            )
            if commit:
                db.session.commit()
        except SQLAlchemyError:
            if commit:
                db.session.rollback()
            raise DAODeleteFailedError()

    @staticmethod
    def validate_update_uniqueness(
        layer_id: int, short_descr: str, annotation_id: Optional[int] = None
    ) -> bool:
        """
        Validate if this annotation short description is unique. `id` is optional
        and serves for validating on updates

        :param short_descr: The annotation short description
        :param layer_id: The annotation layer current id
        :param annotation_id: This annotation is (only for validating on updates)
        :return: bool
        """
        query = db.session.query(Annotation).filter(
            Annotation.short_descr == short_descr, Annotation.layer_id == layer_id
        )
        if annotation_id:
            query = query.filter(Annotation.id != annotation_id)
        return not db.session.query(query.exists()).scalar()
