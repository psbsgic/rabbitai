import logging
from typing import List, Optional, Union

from sqlalchemy.exc import SQLAlchemyError

from rabbitai.dao.base import BaseDAO
from rabbitai.dao.exceptions import DAODeleteFailedError
from rabbitai.extensions import db
from rabbitai.models.annotations import Annotation, AnnotationLayer

logger = logging.getLogger(__name__)


class AnnotationLayerDAO(BaseDAO):
    model_cls = AnnotationLayer

    @staticmethod
    def bulk_delete(
        models: Optional[List[AnnotationLayer]], commit: bool = True
    ) -> None:
        item_ids = [model.id for model in models] if models else []
        try:
            db.session.query(AnnotationLayer).filter(
                AnnotationLayer.id.in_(item_ids)
            ).delete(synchronize_session="fetch")
            if commit:
                db.session.commit()
        except SQLAlchemyError:
            if commit:
                db.session.rollback()
            raise DAODeleteFailedError()

    @staticmethod
    def has_annotations(model_id: Union[int, List[int]]) -> bool:
        if isinstance(model_id, list):
            return (
                db.session.query(AnnotationLayer)
                .filter(AnnotationLayer.id.in_(model_id))
                .join(Annotation)
                .first()
            ) is not None
        return (
            db.session.query(AnnotationLayer)
            .filter(AnnotationLayer.id == model_id)
            .join(Annotation)
            .first()
        ) is not None

    @staticmethod
    def validate_update_uniqueness(name: str, layer_id: Optional[int] = None) -> bool:
        """
        Validate if this layer name is unique. `layer_id` is optional
        and serves for validating on updates

        :param name: The annotation layer name
        :param layer_id: The annotation layer current id
        (only for validating on updates)
        :return: bool
        """
        query = db.session.query(AnnotationLayer).filter(AnnotationLayer.name == name)
        if layer_id:
            query = query.filter(AnnotationLayer.id != layer_id)
        return not db.session.query(query.exists()).scalar()
