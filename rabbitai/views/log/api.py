from flask import current_app as app
from flask_appbuilder.hooks import before_request
from flask_appbuilder.models.sqla.interface import SQLAInterface

import rabbitai.models.core as models
from rabbitai.views.base_api import BaseRabbitaiModelRestApi

from ...constants import MODEL_API_RW_METHOD_PERMISSION_MAP
from . import LogMixin


class LogRestApi(LogMixin, BaseRabbitaiModelRestApi):
    """日志RestApi，提供Log对象关系模型的CRUD。"""

    datamodel = SQLAInterface(models.Log)
    include_route_methods = {"get_list", "get", "post"}
    class_permission_name = "Log"
    method_permission_name = MODEL_API_RW_METHOD_PERMISSION_MAP
    resource_name = "log"
    allow_browser_login = True
    list_columns = [
        "user.username",
        "action",
        "dttm",
        "json",
        "slice_id",
        "dashboard_id",
        "user_id",
        "duration_ms",
        "referrer",
    ]
    show_columns = list_columns

    @staticmethod
    def is_enabled() -> bool:
        return app.config["FAB_ADD_SECURITY_VIEWS"] and app.config["RABBITAI_LOG_VIEW"]

    @before_request
    def ensure_enabled(self) -> None:
        if not self.is_enabled():
            return self.response_404()
        return None
