# -*- coding: utf-8 -*-

from flask import current_app as app
from flask_appbuilder.hooks import before_request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from werkzeug.exceptions import NotFound

import rabbitai.models.core as models
from rabbitai.constants import MODEL_VIEW_RW_METHOD_PERMISSION_MAP, RouteMethod
from rabbitai.views.base import RabbitaiModelView

from . import LogMixin


class LogModelView(LogMixin, RabbitaiModelView):
    datamodel = SQLAInterface(models.Log)
    include_route_methods = {RouteMethod.LIST, RouteMethod.SHOW}
    class_permission_name = "Log"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    @staticmethod
    def is_enabled() -> bool:
        return app.config["FAB_ADD_SECURITY_VIEWS"] and app.config["RABBITAI_LOG_VIEW"]

    @before_request
    def ensure_enabled(self) -> None:
        if not self.is_enabled():
            raise NotFound()
