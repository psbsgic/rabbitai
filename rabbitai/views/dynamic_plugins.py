# -*- coding: utf-8 -*-

from typing import Optional

from flask import make_response, Response
from flask_appbuilder import ModelView
from flask_appbuilder.hooks import before_request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from rabbitai import is_feature_enabled
from rabbitai.constants import MODEL_API_RW_METHOD_PERMISSION_MAP
from rabbitai.models.dynamic_plugins import DynamicPlugin


class DynamicPluginsView(ModelView):
    """Dynamic plugin crud views -- To be replaced by fancy react UI"""

    route_base = "/dynamic-plugins"
    datamodel = SQLAInterface(DynamicPlugin)
    class_permission_name = "DynamicPlugin"

    method_permission_name = MODEL_API_RW_METHOD_PERMISSION_MAP

    add_columns = ["name", "key", "bundle_url"]
    edit_columns = add_columns
    show_columns = add_columns + ["id"]
    list_columns = show_columns

    label_columns = {"name": "插件名称", "key": "唯一标识", "bundle_url": "包地址"}

    description_columns = {
        "name": _("A human-friendly name"),
        "key": _(
            "Used internally to identify the plugin. "
            "Should be set to the package name from the pluginʼs package.json"
        ),
        "bundle_url": _(
            "A full URL pointing to the location "
            "of the built plugin (could be hosted on a CDN for example)"
        ),
    }

    list_title = _("Custom Plugins")
    show_title = _("Custom Plugin")
    add_title = _("Add a Plugin")
    edit_title = _("Edit Plugin")

    @before_request
    def ensure_dynamic_plugins_enabled(self) -> Optional[Response]:
        if not is_feature_enabled("DYNAMIC_PLUGINS"):
            return make_response("Not found", 404)
        return None
