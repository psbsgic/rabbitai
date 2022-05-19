# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from flask import Flask
from sqlalchemy import TypeDecorator
from sqlalchemy_utils import EncryptedType


class AbstractEncryptedFieldAdapter(ABC):
    """加密字段适配器抽象基类。"""

    @abstractmethod
    def create(
        self,
        app_config: Optional[Dict[str, Any]],
        *args: List[Any],
        **kwargs: Optional[Dict[str, Any]]
    ) -> TypeDecorator:
        """
        创建并返回加密字段类型。

        :param app_config: 应用配置对象。
        :param args: 位置参数。
        :param kwargs: 关键字参数。
        :return:
        """
        pass


class SQLAlchemyUtilsAdapter(AbstractEncryptedFieldAdapter):
    """加密字段适配器，提供依据应用配置的 SECRET_KEY 构建 EncryptedType 类型实例的方法：create。"""

    def create(
        self,
        app_config: Optional[Dict[str, Any]],
        *args: List[Any],
        **kwargs: Optional[Dict[str, Any]]
    ) -> TypeDecorator:
        """
        创建并返回加密字段类型。

        :param app_config: 应用配置对象。
        :param args: 位置参数。
        :param kwargs: 关键字参数。
        :return:
        """

        if app_config:
            return EncryptedType(*args, app_config["SECRET_KEY"], **kwargs)

        raise Exception("Missing app_config kwarg")


class EncryptedFieldFactory:
    """加密字段工厂，依据应用配置对象 SQLALCHEMY_ENCRYPTED_FIELD_TYPE_ADAPTER 提供的适配器创建加密字段的方法。"""

    def __init__(self) -> None:
        self._concrete_type_adapter: Optional[AbstractEncryptedFieldAdapter] = None
        self._config: Optional[Dict[str, Any]] = None

    def init_app(self, app: Flask) -> None:
        """
        使用指定Flask应用实例初始化该对象，读取加密相关配置。

        :param app: Flask应用实例。
        :return:
        """

        self._config = app.config
        self._concrete_type_adapter = self._config["SQLALCHEMY_ENCRYPTED_FIELD_TYPE_ADAPTER"]()

    def create(
        self, *args: List[Any], **kwargs: Optional[Dict[str, Any]]
    ) -> TypeDecorator:
        """
        创建并返回一个加密字段类型。

        :param args:
        :param kwargs:
        :return:
        """

        if self._concrete_type_adapter:
            return self._concrete_type_adapter.create(self._config, *args, **kwargs)

        raise Exception("App not initialized yet. Please call init_app first")
