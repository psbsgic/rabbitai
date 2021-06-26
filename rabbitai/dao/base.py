from typing import Any, Dict, List, Optional, Type

from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla import Model
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from rabbitai.dao.exceptions import (
    DAOConfigError,
    DAOCreateFailedError,
    DAODeleteFailedError,
    DAOUpdateFailedError,
)
from rabbitai.extensions import db


class BaseDAO:
    """基本 DAO, 实现基本的 CRUD sqlalchemy 操作。"""

    model_cls: Optional[Type[Model]] = None
    """对象关系模型的类型，子类需要状态化模型类，以便它们不需要实现基本的 create, update, delete 等方法"""
    base_filter: Optional[BaseFilter] = None
    """基本过滤器，子类可以注册基本过滤器以便应用于所有过滤方法。"""

    @classmethod
    def find_by_id(cls, model_id: int, session: Session = None) -> Model:
        """
        依据指定标识查找相应的模型，如果定义 `base_filter` 则应用它。

        :param model_id: 模型标识。
        :param session: 数据库会话。
        :return:
        """

        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, session)
            query = cls.base_filter("id", data_model).apply(query, None)

        return query.filter_by(id=model_id).one_or_none()

    @classmethod
    def find_by_ids(cls, model_ids: List[int]) -> List[Model]:
        """
        依据指定标识列表查找相应的模型，如果定义 `base_filter` 则应用它。

        :param model_ids: 模型标识列表。
        :return: 模型列表。
        """

        id_col = getattr(cls.model_cls, "id", None)
        if id_col is None:
            return []

        query = db.session.query(cls.model_cls).filter(id_col.in_(model_ids))
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(query, None)

        return query.all()

    @classmethod
    def find_all(cls) -> List[Model]:
        """返回所有对象模型。"""
        query = db.session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(query, None)
        return query.all()

    @classmethod
    def create(cls, properties: Dict[str, Any], commit: bool = True) -> Model:
        """
        创建并返回对象模型。

        :raises: DAOCreateFailedError
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        model = cls.model_cls()
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            db.session.add(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise DAOCreateFailedError(exception=ex)
        return model

    @classmethod
    def update(
        cls, model: Model, properties: Dict[str, Any], commit: bool = True
    ) -> Model:
        """
        更新指定对象模型。

        :raises: DAOCreateFailedError
        """
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            db.session.merge(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise DAOUpdateFailedError(exception=ex)
        return model

    @classmethod
    def delete(cls, model: Model, commit: bool = True) -> Model:
        """
        删除指定对象模型。

        :raises: DAOCreateFailedError
        """
        try:
            db.session.delete(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise DAODeleteFailedError(exception=ex)
        return model
