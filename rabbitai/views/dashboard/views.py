import re
from typing import List, Union

from flask import g, redirect, request, Response
from flask_appbuilder import expose
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from flask_babel import gettext as __, lazy_gettext as _

from rabbitai import db, event_logger, is_feature_enabled
from rabbitai.constants import MODEL_VIEW_RW_METHOD_PERMISSION_MAP, RouteMethod
from rabbitai.models.dashboard import Dashboard as DashboardModel
from rabbitai.typing import FlaskResponse
from rabbitai.utils import core as utils
from rabbitai.views.base import (
    BaseRabbitaiView,
    check_ownership,
    DeleteMixin,
    generate_download_headers,
    RabbitaiModelView,
)
from rabbitai.views.dashboard.mixin import DashboardMixin


class DashboardModelView(DashboardMixin, RabbitaiModelView, DeleteMixin):
    """仪表盘模型视图。"""

    route_base = "/dashboard"
    datamodel = SQLAInterface(DashboardModel)
    # TODO disable api_read and api_delete (used by cypress)
    # once we move to ChartRestModelApi
    class_permission_name = "Dashboard"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    include_route_methods = RouteMethod.CRUD_SET | {
        RouteMethod.API_READ,
        RouteMethod.API_DELETE,
        "download_dashboards",
    }

    @has_access
    @expose("/list/")
    def list(self) -> FlaskResponse:
        if not is_feature_enabled("ENABLE_REACT_CRUD_VIEWS"):
            return super().list()

        return super().render_app_template()

    @action("mulexport", __("Export"), __("Export dashboards?"), "fa-database")
    def mulexport(
        self, items: Union["DashboardModelView", List["DashboardModelView"]]
    ) -> FlaskResponse:
        if not isinstance(items, list):
            items = [items]
        ids = "".join("&id={}".format(d.id) for d in items)
        return redirect("/dashboard/export_dashboards_form?{}".format(ids[1:]))

    @event_logger.log_this
    @has_access
    @expose("/export_dashboards_form")
    def download_dashboards(self) -> FlaskResponse:
        if request.args.get("action") == "go":
            ids = request.args.getlist("id")
            return Response(
                DashboardModel.export_dashboards(ids),
                headers=generate_download_headers("json"),
                mimetype="application/text",
            )
        return self.render_template(
            "rabbitai/export_dashboards.html", dashboards_url="/dashboard/list"
        )

    def pre_add(self, item: "DashboardModelView") -> None:
        item.slug = item.slug or None
        if item.slug:
            item.slug = item.slug.strip()
            item.slug = item.slug.replace(" ", "-")
            item.slug = re.sub(r"[^\w\-]+", "", item.slug)
        if g.user not in item.owners:
            item.owners.append(g.user)
        utils.validate_json(item.json_metadata)
        utils.validate_json(item.position_json)
        owners = list(item.owners)
        for slc in item.slices:
            slc.owners = list(set(owners) | set(slc.owners))

    def pre_update(self, item: "DashboardModelView") -> None:
        check_ownership(item)
        self.pre_add(item)


class Dashboard(BaseRabbitaiView):
    """仪表盘视图基类。"""

    class_permission_name = "Dashboard"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    @has_access
    @expose("/new/")
    def new(self) -> FlaskResponse:  # pylint: disable=no-self-use
        """Creates a new, blank dashboard and redirects to it in edit mode"""
        new_dashboard = DashboardModel(
            dashboard_title="[ untitled dashboard ]", owners=[g.user]
        )
        db.session.add(new_dashboard)
        db.session.commit()
        return redirect(f"/rabbitai/dashboard/{new_dashboard.id}/?edit=true")


class DashboardModelViewAsync(DashboardModelView):
    """异步仪表盘视图。"""

    route_base = "/dashboardasync"
    class_permission_name = "Dashboard"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    include_route_methods = {RouteMethod.API_READ}

    list_columns = [
        "id",
        "dashboard_link",
        "creator",
        "modified",
        "dashboard_title",
        "changed_on",
        "url",
        "changed_by_name",
    ]
    label_columns = {
        "dashboard_link": _("Dashboard"),
        "dashboard_title": _("Title"),
        "creator": _("Creator"),
        "modified": _("Modified"),
    }
