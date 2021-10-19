# -*- coding: utf-8 -*-

from markupsafe import Markup
from flask_babel import lazy_gettext as _

from rabbitai.dashboards.filters import DashboardAccessFilter
from rabbitai.views.chart.filters import SliceFilter


class SliceMixin:
    """切片视图混入类，定义切片视图相关的属性。"""

    list_title = _("Charts")
    show_title = _("Show Chart")
    add_title = _("Add Chart")
    edit_title = _("Edit Chart")

    can_add = False
    search_columns = (
        "slice_name",
        "description",
        "viz_type",
        "datasource_name",
        "owners",
    )
    list_columns = ["slice_link", "viz_type", "datasource_link", "creator", "modified"]
    order_columns = [
        "slice_name",
        "viz_type",
        "datasource_link",
        "modified",
        "changed_on",
    ]
    edit_columns = [
        "slice_name",
        "description",
        "viz_type",
        "owners",
        "dashboards",
        "params",
        "cache_timeout",
    ]
    base_order = ("changed_on", "desc")
    description_columns = {
        "description": Markup(
            "该内容显示为仪表盘视图中部件标头。"
            "支持"
            '<a href="https://daringfireball.net/projects/markdown/"">'
            "markdown</a>"
        ),
        "params": _(
            "These parameters are generated dynamically when clicking "
            "the save or overwrite button in the explore view. This JSON "
            "object is exposed here for reference and for power users who may "
            "want to alter specific parameters."
        ),
        "cache_timeout": _(
            "Duration (in seconds) of the caching timeout for this chart. "
            "Note this defaults to the datasource/table timeout if undefined."
        ),
    }
    base_filters = [["id", SliceFilter, lambda: []]]
    label_columns = {
        "cache_timeout": _("Cache Timeout"),
        "creator": _("Creator"),
        "dashboards": _("Dashboards"),
        "datasource_link": _("Datasource"),
        "description": _("Description"),
        "modified": _("Last Modified"),
        "owners": _("Owners"),
        "params": _("Parameters"),
        "slice_link": _("Chart"),
        "slice_name": _("Name"),
        "table": _("Table"),
        "viz_type": _("Visualization Type"),
    }

    add_form_query_rel_fields = {"dashboards": [["name", DashboardAccessFilter, None]]}

    edit_form_query_rel_fields = add_form_query_rel_fields
