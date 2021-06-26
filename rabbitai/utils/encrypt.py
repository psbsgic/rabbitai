# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from flask import Flask
from sqlalchemy import TypeDecorator
from sqlalchemy_utils import EncryptedType


class AbstractEncryptedFieldAdapter(ABC):
    @abstractmethod
    def create(
        self,
        app_config: Optional[Dict[str, Any]],
        *args: List[Any],
        **kwargs: Optional[Dict[str, Any]]
    ) -> TypeDecorator:
        pass


class SQLAlchemyUtilsAdapter(AbstractEncryptedFieldAdapter):
    def create(
        self,
        app_config: Optional[Dict[str, Any]],
        *args: List[Any],
        **kwargs: Optional[Dict[str, Any]]
    ) -> TypeDecorator:
        if app_config:
            return EncryptedType(*args, app_config["SECRET_KEY"], **kwargs)

        raise Exception("Missing app_config kwarg")


class EncryptedFieldFactory:
    """加密字段工厂。"""

    def __init__(self) -> None:
        self._concrete_type_adapter: Optional[AbstractEncryptedFieldAdapter] = None
        self._config: Optional[Dict[str, Any]] = None

    def init_app(self, app: Flask) -> None:
        """
        初始化该工厂，从app配置对象中获取 SQLALCHEMY_ENCRYPTED_FIELD_TYPE_ADAPTER。

        :param app:
        :return:
        """
        self._config = app.config
        self._concrete_type_adapter = self._config[
            "SQLALCHEMY_ENCRYPTED_FIELD_TYPE_ADAPTER"
        ]()

    def create(self, *args: List[Any], **kwargs: Optional[Dict[str, Any]]) -> TypeDecorator:
        if self._concrete_type_adapter:
            return self._concrete_type_adapter.create(self._config, *args, **kwargs)

        raise Exception("App not initialized yet. Please call init_app first")
