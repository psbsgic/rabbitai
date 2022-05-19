# -*- coding: utf-8 -*-

import json
from typing import Any, List, Optional

from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from wtforms import Field


class JsonListField(Field):
    """编辑和显示Json列表字段，继承：Field，使用 BS3TextFieldWidget 显示数据。"""

    widget = BS3TextFieldWidget()
    """显示数据的小部件"""
    data: List[str] = []
    """数据，字符串的列表"""

    def _value(self) -> str:
        return json.dumps(self.data)

    def process_formdata(self, valuelist: List[str]) -> None:
        """
        处理表单数据。

        :param valuelist: 字符串的列表。
        :return:
        """

        if valuelist and valuelist[0]:
            self.data = json.loads(valuelist[0])
        else:
            self.data = []


class CommaSeparatedListField(Field):
    """编辑和显示逗号分隔列表字段。"""

    widget = BS3TextFieldWidget()
    """显示数据的小部件"""
    data: List[str] = []
    """数据，字符串的列表"""

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
    """
    返回非空值的列表或None。

    :param values:
    :return: 非空值的列表或None。
    """

    if not values:
        return None

    data = [value for value in values if value]
    if not data:
        return None

    return data
