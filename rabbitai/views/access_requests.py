# -*- coding: utf-8 -*-

from flask import current_app as app
from flask_appbuilder.hooks import before_request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import NotFound

from rabbitai.constants import RouteMethod
from rabbitai.views.base import DeleteMixin, RabbitaiModelView
from rabbitai.views.core import DAR


class AccessRequestsModelView(RabbitaiModelView, DeleteMixin):
    """访问请求模型视图。"""

    datamodel = SQLAInterface(DAR)
    include_route_methods = RouteMethod.CRUD_SET
    list_columns = [
        "username",
        "user_roles",
        "datasource_link",
        "roles_with_datasource",
        "created_on",
    ]
    order_columns = ["created_on"]
    base_order = ("changed_on", "desc")
    label_columns = {
        "username": _("User"),
        "user_roles": _("User Roles"),
        "database": _("Database URL"),
        "datasource_link": _("Datasource"),
        "roles_with_datasource": _("Roles to grant"),
        "created_on": _("Created On"),
    }

    @staticmethod
    def is_enabled() -> bool:
        return bool(app.config["ENABLE_ACCESS_REQUEST"])

    @before_request
    def ensure_enabled(self) -> None:
        if not self.is_enabled():
            raise NotFound()
