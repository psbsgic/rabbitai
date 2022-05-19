# -*- coding: utf-8 -*-

"""不同数据库引擎的兼容层

此模块存储特定于不同数据库引擎的逻辑。
类似但不完全相同的与时间相关的函数，或者关于是否公开某些功能以及如何公开这些功能的信息。

例如，Hive/Presto支持分区，并且有一个特定的API来列出分区。
其他数据库（如Vertica）也支持分区，但使用不同的API访问分区。
其他数据库根本不支持分区。这里的类将使用一个公共接口来指定所有这些。

一般的想法是使用静态类和继承方案。
"""

import inspect
import logging
import pkgutil
from collections import defaultdict
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, List, Set, Type

import sqlalchemy.databases
import sqlalchemy.dialects
from pkg_resources import iter_entry_points
from sqlalchemy.engine.default import DefaultDialect

from rabbitai.db_engine_specs.base import BaseEngineSpec

logger = logging.getLogger(__name__)


def is_engine_spec(attr: Any) -> bool:
    """是否引擎规范，即是否 BaseEngineSpec 的派生类。"""

    return (
        inspect.isclass(attr)
        and issubclass(attr, BaseEngineSpec)
        and attr != BaseEngineSpec
    )


def load_engine_specs() -> List[Type[BaseEngineSpec]]:
    """加载并返回该模块定义的数据库引擎规范，即该文件所在目录下（rabbitai）的各模块，以及外部定义的模块。"""

    engine_specs: List[Type[BaseEngineSpec]] = []
    """引擎规范列表，即 BaseEngineSpec 及其派生类型实例的列表"""

    # 加载该应用定义的数据库引擎规范
    db_engine_spec_dir = str(Path(__file__).parent)
    for module_info in pkgutil.iter_modules([db_engine_spec_dir], prefix="."):
        module = import_module(module_info.name, package=__name__)
        engine_specs.extend(
            getattr(module, attr)
            for attr in module.__dict__
            if is_engine_spec(getattr(module, attr))
        )

    # 加载外部定义的数据库引擎
    for ep in iter_entry_points("rabbitai.db_engine_specs"):
        try:
            engine_spec = ep.load()
        except Exception:
            logger.warning("Unable to load Rabbitai DB engine spec: %s", engine_spec)
            continue
        engine_specs.append(engine_spec)

    return engine_specs


def get_engine_specs() -> Dict[str, Type[BaseEngineSpec]]:
    """返回该模块定义的数据库引擎规范的字典（名称和实例）。"""

    engine_specs = load_engine_specs()

    # build map from name/alias -> spec
    engine_specs_map: Dict[str, Type[BaseEngineSpec]] = {}
    for engine_spec in engine_specs:
        names = [engine_spec.engine]
        if engine_spec.engine_aliases:
            names.extend(engine_spec.engine_aliases)

        for name in names:
            engine_specs_map[name] = engine_spec

    return engine_specs_map


def get_available_engine_specs() -> Dict[Type[BaseEngineSpec], Set[str]]:
    """
    返回可用的引擎规格和安装的驱动程序。
    """

    drivers: Dict[str, Set[str]] = defaultdict(set)

    # native SQLAlchemy dialects
    for attr in sqlalchemy.databases.__all__:
        dialect = getattr(sqlalchemy.dialects, attr)
        for attribute in dialect.__dict__.values():
            if (
                hasattr(attribute, "dialect")
                and inspect.isclass(attribute.dialect)
                and issubclass(attribute.dialect, DefaultDialect)
            ):
                try:
                    attribute.dialect.dbapi()
                except ModuleNotFoundError:
                    continue
                except Exception as ex:
                    logger.warning(
                        "Unable to load dialect %s: %s", attribute.dialect, ex
                    )
                    continue
                drivers[attr].add(attribute.dialect.driver)

    # installed 3rd-party dialects
    for ep in iter_entry_points("sqlalchemy.dialects"):
        try:
            dialect = ep.load()
        except Exception:
            logger.warning("Unable to load SQLAlchemy dialect: %s", dialect)
        else:
            backend = dialect.name
            if isinstance(backend, bytes):
                backend = backend.decode()
            driver = getattr(dialect, "driver", dialect.name)
            if isinstance(driver, bytes):
                driver = driver.decode()
            drivers[backend].add(driver)

    available_engines = {}
    for engine_spec in load_engine_specs():
        available_engines[engine_spec] = drivers[engine_spec.engine]

    return available_engines
