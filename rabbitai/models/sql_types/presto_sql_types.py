from typing import Any, Dict, List, Optional, Type

from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.sql.visitors import Visitable

# _compiler_dispatch is defined to help with type compilation


class TinyInteger(Integer):
    """
    A type for tiny ``int`` integers.
    """

    @property
    def python_type(self) -> Type[int]:
        return int

    @classmethod
    def _compiler_dispatch(cls, _visitor: Visitable, **_kw: Any) -> str:
        return "TINYINT"


class Interval(TypeEngine):
    """
    A type for intervals.
    """

    @property
    def python_type(self) -> Optional[Type[Any]]:
        return None

    @classmethod
    def _compiler_dispatch(cls, _visitor: Visitable, **_kw: Any) -> str:
        return "INTERVAL"


class Array(TypeEngine):
    """
    A type for arrays.
    """

    @property
    def python_type(self) -> Optional[Type[List[Any]]]:
        return list

    @classmethod
    def _compiler_dispatch(cls, _visitor: Visitable, **_kw: Any) -> str:
        return "ARRAY"


class Map(TypeEngine):
    """
    A type for maps.
    """

    @property
    def python_type(self) -> Optional[Type[Dict[Any, Any]]]:
        return dict

    @classmethod
    def _compiler_dispatch(cls, _visitor: Visitable, **_kw: Any) -> str:
        return "MAP"


class Row(TypeEngine):
    """
    A type for rows.
    """

    @property
    def python_type(self) -> Optional[Type[Any]]:
        return None

    @classmethod
    def _compiler_dispatch(cls, _visitor: Visitable, **_kw: Any) -> str:
        return "ROW"
