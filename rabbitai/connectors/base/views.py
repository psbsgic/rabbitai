# -*- coding: utf-8 -*-

from typing import Any

from flask import Markup
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget

from rabbitai.connectors.base.models import BaseDatasource
from rabbitai.exceptions import RabbitaiException
from rabbitai.views.base import RabbitaiModelView


class BS3TextFieldROWidget(BS3TextFieldWidget):
    """自定义只读文本字段小部件。"""

    def __call__(self, field: Any, **kwargs: Any) -> Markup:
        kwargs["readonly"] = "true"
        return super().__call__(field, **kwargs)


class DatasourceModelView(RabbitaiModelView):
    """数据源模型视图，提供数据源模型的显示、编辑等操作的界面。"""

    def pre_delete(self, item: BaseDatasource) -> None:
        if item.slices:
            raise RabbitaiException(
                Markup(
                    "不能删除还有图表使用的数据源。"
                    "关联以下图表："
                    + "".join([i.slice_name for i in item.slices])
                )
            )
