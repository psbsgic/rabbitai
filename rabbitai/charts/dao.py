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
    """图表数据访问对象，提供 Slice 模型对象的数据库CRUD操作。"""

    model_cls = Slice
    base_filter = ChartFilter

    @staticmethod
    def bulk_delete(models: Optional[List[Slice]], commit: bool = True) -> None:
        """
        从数据库中批量删除指定切片对象关系模型对应的记录。

        :param models: 要删除的切片对象关系模型。
        :param commit:
        :return:
        """
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
        """
        保存指定数据模型到数据库。

        :param slc:
        :param commit:
        :return:
        """
        db.session.add(slc)
        if commit:
            db.session.commit()

    @staticmethod
    def overwrite(slc: Slice, commit: bool = True) -> None:
        """
        更新到数据库。

        :param slc:
        :param commit:
        :return:
        """
        db.session.merge(slc)
        if commit:
            db.session.commit()

    @staticmethod
    def favorited_ids(charts: List[Slice], current_user_id: int) -> List[FavStar]:
        """
        返回关注者标识。

        :param charts:
        :param current_user_id:
        :return:
        """
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
