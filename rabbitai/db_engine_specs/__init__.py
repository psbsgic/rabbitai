"""Compatibility layer for different database engines

This modules stores logic specific to different database engines. Things
like time-related functions that are similar but not identical, or
information as to expose certain features or not and how to expose them.

For instance, Hive/Presto supports partitions and have a specific API to
list partitions. Other databases like Vertica also support partitions but
have different API to get to them. Other databases don't support partitions
at all. The classes here will use a common interface to specify all this.

The general idea is to use static classes and an inheritance scheme.
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
    return (
        inspect.isclass(attr)
        and issubclass(attr, BaseEngineSpec)
        and attr != BaseEngineSpec
    )


def get_engine_specs() -> Dict[str, Type[BaseEngineSpec]]:
    """
    获取数据库引擎规范，从当前目录加载所有 BaseEngineSpec 的派生类。

    :return:
    """

    engine_specs: List[Type[BaseEngineSpec]] = []

    # load standard engines
    db_engine_spec_dir = str(Path(__file__).parent)
    for module_info in pkgutil.iter_modules([db_engine_spec_dir], prefix="."):
        module = import_module(module_info.name, package=__name__)
        engine_specs.extend(
            getattr(module, attr)
            for attr in module.__dict__
            if is_engine_spec(getattr(module, attr))
        )

    # load additional engines from external modules
    for ep in iter_entry_points("rabbitai.db_engine_specs"):
        try:
            engine_spec = ep.load()
        except Exception:
            logger.warning("Unable to load Rabbitai DB engine spec: %s", engine_spec)
            continue
        engine_specs.append(engine_spec)

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
    """返回可用的发动机规格和安装的驱动程序。"""

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
                except Exception as ex:  # pylint: disable=broad-except
                    logger.warning(
                        "Unable to load dialect %s: %s", attribute.dialect, ex
                    )
                    continue
                drivers[attr].add(attribute.dialect.driver)

    # installed 3rd-party dialects
    for ep in iter_entry_points("sqlalchemy.dialects"):
        try:
            dialect = ep.load()
        except Exception:  # pylint: disable=broad-except
            logger.warning("Unable to load SQLAlchemy dialect: %s", dialect)
        else:
            drivers[dialect.name].add(dialect.driver)

    engine_specs = get_engine_specs()
    return {
        engine_specs[backend]: drivers
        for backend, drivers in drivers.items()
        if backend in engine_specs
    }
