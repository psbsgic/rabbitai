# -*- coding: utf-8 -*-

from typing import Any, List

from werkzeug.routing import BaseConverter, Map

from rabbitai.models.tags import ObjectTypes


class RegexConverter(BaseConverter):
    """正则表达式转换器。"""

    def __init__(self, url_map: Map, *items: List[str]) -> None:
        super(RegexConverter, self).__init__(url_map)  # type: ignore
        self.regex = items[0]


class ObjectTypeConverter(BaseConverter):
    """Validate that object_type is indeed an object type."""

    def to_python(self, value: str) -> Any:
        return ObjectTypes[value]

    def to_url(self, value: Any) -> str:
        return value.name
