# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Callable, Type, TYPE_CHECKING

from flask_babel import gettext as __
from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect

if TYPE_CHECKING:
    from rabbitai.db_engine_specs.base import BaseEngineSpec


def literal_dttm_type_factory(
    sqla_type: Type[types.TypeEngine],
    db_engine_spec: Type["BaseEngineSpec"],
    col_type: str,
) -> Type[types.TypeEngine]:
    """
    创建支持 datetime 文字绑定的自定义SQLAlchemy类型。

    :param sqla_type: 要扩展的 SQL类型。
    :param db_engine_spec: 支持 `convert_dttm` 方法的数据库引擎规范。
    :param col_type: 在数据表元数据中定义的原生列类型。
    :return: 支持 datetime 文字绑定的自定义SQLAlchemy类型。
    """

    class TemporalWrapperType(sqla_type):

        def literal_processor(self, dialect: Dialect) -> Callable[[Any], Any]:
            def process(value: Any) -> Any:
                if isinstance(value, datetime):
                    ts_expression = db_engine_spec.convert_dttm(col_type, value)
                    if ts_expression is None:
                        raise NotImplementedError(
                            __(
                                "Temporal expression not supported for type: "
                                "%(col_type)s",
                                col_type=col_type,
                            )
                        )
                    return ts_expression
                return super().process(value)

            return process

    return TemporalWrapperType
