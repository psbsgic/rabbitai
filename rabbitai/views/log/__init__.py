from flask_babel import lazy_gettext as _


class LogMixin:
    """日志混入类，定义Log模型视图相关字段。"""

    list_title = _("Logs")
    show_title = _("Show Log")
    add_title = _("Add Log")
    edit_title = _("Edit Log")

    list_columns = ["user", "action", "dttm"]
    edit_columns = ["user", "action", "dttm", "json"]
    base_order = ("dttm", "desc")
    label_columns = {
        "user": _("User"),
        "action": _("Action"),
        "dttm": _("dttm"),
        "json": _("JSON"),
    }
