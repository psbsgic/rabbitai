import logging
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

from rabbitai.charts.filters import ChartFilter
from rabbitai.dao.base import BaseDAO
from rabbitai.extensions import db
from rabbitai.models.core import FavStar, FavStarClassName
from rabbitai.models.slice import Slice

if TYPE_CHECKING:
    from rabbitai.connectors.base.models import BaseDatasource

logger = logging.getLogger(__name__)


class ChartDAO(BaseDAO):
    model_cls = Slice
    base_filter = ChartFilter

    @staticmethod
    def bulk_delete(models: Optional[List[Slice]], commit: bool = True) -> None:
        item_ids = [model.id for model in models] if models else []
        # bulk delete, first delete related data
        if models:
            for model in models:
                model.owners = []
                model.dashboards = []
                db.session.merge(model)
        # bulk delete itself
        try:
            db.session.query(Slice).filter(Slice.id.in_(item_ids)).delete(
                synchronize_session="fetch"
            )
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:
            if commit:
                db.session.rollback()
            raise ex

    @staticmethod
    def save(slc: Slice, commit: bool = True) -> None:
        db.session.add(slc)
        if commit:
            db.session.commit()

    @staticmethod
    def overwrite(slc: Slice, commit: bool = True) -> None:
        db.session.merge(slc)
        if commit:
            db.session.commit()

    @staticmethod
    def favorited_ids(charts: List[Slice], current_user_id: int) -> List[FavStar]:
        ids = [chart.id for chart in charts]
        return [
            star.obj_id
            for star in db.session.query(FavStar.obj_id)
            .filter(
                FavStar.class_name == FavStarClassName.CHART,
                FavStar.obj_id.in_(ids),
                FavStar.user_id == current_user_id,
            )
            .all()
        ]
