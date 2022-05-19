# -*- coding: utf-8 -*-

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
    """基础数据访问对象，使用 sqlalchemy，基于给定模型类型和过滤器实现创建、查找、更新和删除等基本操作。"""

    model_cls: Optional[Type[Model]] = None
    """模型类（Model及其派生类），子类需要声明模型类，这样它们就不需要实现基本的创建、更新和删除方法"""
    base_filter: Optional[BaseFilter] = None
    """基本过滤器类，BaseFilter 的子类，子类可以注册过滤器，以应用到所有过滤方法"""

    @classmethod
    def find_by_id(cls, model_id: int, session: Session = None) -> Model:
        """
        按照指定模型标识从数据库中查找模型实例，自动应用基础过滤器。

        :param model_id: 模型标识。
        :param session: 数据库会话对象，如果未指定则使用 db.session。

        :return: 模型实例。
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
        按照指定模型标识列表从数据库中查找模型实例的列表，自动应用基础过滤器。

        :param model_ids: 模型标识列表。
        :return:
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
        """
        查找所有满足基本过滤条件的模型实例。

        :return:
        """

        query = db.session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(query, None)

        return query.all()

    @classmethod
    def create(cls, properties: Dict[str, Any], commit: bool = True) -> Model:
        """
        依据指定属性字典，创建模型实例，并指定是否提交到数据库。

        :raises: DAOCreateFailedError

        :param properties: 要创建对象模型的属性字典。
        :param commit: 是否提交，默认True。

        :return: 数据模型实例。
        """

        if cls.model_cls is None:
            raise DAOConfigError()
        model = cls.model_cls()  # pylint: disable=not-callable
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            db.session.add(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOCreateFailedError(exception=ex)
        return model

    @classmethod
    def update(cls, model: Model, properties: Dict[str, Any], commit: bool = True) -> Model:
        """
        依据指定属性字典更新模型实例，并指定是否提交到数据库。

        :raises: DAOCreateFailedError

        :param model: 要更新的对象模型。
        :param properties: 要创建对象模型的属性字典。
        :param commit: 是否提交，默认True。

        :return: 更新后的对象模型。
        """

        for key, value in properties.items():
            setattr(model, key, value)
        try:
            db.session.merge(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOUpdateFailedError(exception=ex)
        return model

    @classmethod
    def delete(cls, model: Model, commit: bool = True) -> Model:
        """
        从数据库中删除指定模型。

        :raises: DAOCreateFailedError
        """
        try:
            db.session.delete(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAODeleteFailedError(exception=ex)
        return model
