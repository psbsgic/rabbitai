# -*- coding: utf-8 -*-

import json
from typing import Any, List, Optional

from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from wtforms import Field


class JsonListField(Field):
    """编辑和显示Json列表字段。"""
    widget = BS3TextFieldWidget()
    data: List[str] = []

    def _value(self) -> str:
        return json.dumps(self.data)

    def process_formdata(self, valuelist: List[str]) -> None:
        if valuelist and valuelist[0]:
            self.data = json.loads(valuelist[0])
        else:
            self.data = []


class CommaSeparatedListField(Field):
    """编辑和显示逗号分隔列表字段。"""

    widget = BS3TextFieldWidget()
    data: List[str] = []

    def _value(self) -> str:
        if self.data:
            return ", ".join(self.data)

        return ""

    def process_formdata(self, valuelist: List[str]) -> None:
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(",")]
        else:
            self.data = []


def filter_not_empty_values(values: Optional[List[Any]]) -> Optional[List[Any]]:
    """Returns a list of non empty values or None"""
    if not values:
        return None
    data = [value for value in values if value]
    if not data:
        return None
    return data
