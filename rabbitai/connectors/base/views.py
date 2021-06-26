from typing import Any

from flask import Markup
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget

from rabbitai.connectors.base.models import BaseDatasource
from rabbitai.exceptions import RabbitaiException
from rabbitai.views.base import RabbitaiModelView


class BS3TextFieldROWidget(  # pylint: disable=too-few-public-methods
    BS3TextFieldWidget
):
    """
    Custom read only text field widget.
    """

    def __call__(self, field: Any, **kwargs: Any) -> Markup:
        kwargs["readonly"] = "true"
        return super().__call__(field, **kwargs)


class DatasourceModelView(RabbitaiModelView):
    def pre_delete(self, item: BaseDatasource) -> None:
        if item.slices:
            raise RabbitaiException(
                Markup(
                    "Cannot delete a datasource that has slices attached to it."
                    "Here's the list of associated charts: "
                    + "".join([i.slice_name for i in item.slices])
                )
            )
