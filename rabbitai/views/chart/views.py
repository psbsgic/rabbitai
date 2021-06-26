import json

from flask import g
from flask_appbuilder import expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from rabbitai import db, is_feature_enabled
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.constants import MODEL_VIEW_RW_METHOD_PERMISSION_MAP, RouteMethod
from rabbitai.models.slice import Slice
from rabbitai.typing import FlaskResponse
from rabbitai.utils import core as utils
from rabbitai.views.base import (
    check_ownership,
    common_bootstrap_payload,
    DeleteMixin,
    RabbitaiModelView,
)
from rabbitai.views.chart.mixin import SliceMixin
from rabbitai.views.utils import bootstrap_user_data


class SliceModelView(SliceMixin, RabbitaiModelView, DeleteMixin):
    """切片模型视图，提供切片模型相关的CRUD和界面。"""

    route_base = "/chart"
    datamodel = SQLAInterface(Slice)
    include_route_methods = RouteMethod.CRUD_SET | {
        RouteMethod.DOWNLOAD,
        RouteMethod.API_READ,
        RouteMethod.API_DELETE,
    }
    class_permission_name = "Chart"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    def pre_add(self, item: "SliceModelView") -> None:
        utils.validate_json(item.params)

    def pre_update(self, item: "SliceModelView") -> None:
        utils.validate_json(item.params)
        check_ownership(item)

    def pre_delete(self, item: "SliceModelView") -> None:
        check_ownership(item)

    @expose("/add", methods=["GET", "POST"])
    @has_access
    def add(self) -> FlaskResponse:
        datasources = [
            {"value": str(d.id) + "__" + d.type, "label": repr(d)}
            for d in ConnectorRegistry.get_all_datasources(db.session)
        ]
        payload = {
            "datasources": sorted(
                datasources,
                key=lambda d: d["label"].lower() if isinstance(d["label"], str) else "",
            ),
            "common": common_bootstrap_payload(),
            "user": bootstrap_user_data(g.user),
        }
        return self.render_template(
            "rabbitai/add_slice.html", bootstrap_data=json.dumps(payload)
        )

    @expose("/list/")
    @has_access
    def list(self) -> FlaskResponse:
        if not is_feature_enabled("ENABLE_REACT_CRUD_VIEWS"):
            return super().list()

        return super().render_app_template()


class SliceAsync(SliceModelView):
    """异步切片模型视图。"""

    route_base = "/sliceasync"
    include_route_methods = {RouteMethod.API_READ}

    list_columns = [
        "changed_on",
        "changed_on_humanized",
        "creator",
        "datasource_id",
        "datasource_link",
        "datasource_url",
        "datasource_name_text",
        "datasource_type",
        "description",
        "description_markeddown",
        "edit_url",
        "icons",
        "id",
        "modified",
        "owners",
        "params",
        "slice_link",
        "slice_name",
        "slice_url",
        "viz_type",
    ]
    label_columns = {"icons": " ", "slice_link": _("Chart")}
