# ATTENTION: If you change any constants, make sure to also change utils/common.js

# string to use when None values *need* to be converted to/from strings
from enum import Enum

NULL_STRING = "<NULL>"

# 示例数据库的 UUID
EXAMPLES_DB_UUID = "a2dc77af-e654-49bb-b321-40f6b559a1ee"


class RouteMethod:
    """
    路由方法是 FAB 中围绕 ModelView 和 RestModelView 类的一个 FAB 概念。
    派生类可以将 `include_route_method` 和 `exclude_route_methods` 类属性定义为一组将公开或不公开的方法。

    这个类是静态常量的集合，用于查阅公共路由方法，即在 FAB 中的基类中定义的方法。
    """

    # region ModelView specific

    ACTION = "action"
    ACTION_POST = "action_post"
    ADD = "add"
    DELETE = "delete"
    DOWNLOAD = "download"
    EDIT = "edit"
    LIST = "list"
    SHOW = "show"
    INFO = "info"

    API_CREATE = "api_create"
    API_DELETE = "api_delete"
    API_GET = "api_get"
    API_READ = "api_read"
    API_UPDATE = "api_update"

    # endregion

    # region RestModelView specific

    EXPORT = "export"
    IMPORT = "import_"
    GET = "get"
    GET_LIST = "get_list"
    POST = "post"
    PUT = "put"
    RELATED = "related"
    DISTINCT = "distinct"

    # endregion

    # region Commonly used sets

    API_SET = {API_CREATE, API_DELETE, API_GET, API_READ, API_UPDATE}
    """API相关路由集合，{API_CREATE, API_DELETE, API_GET, API_READ, API_UPDATE}"""
    CRUD_SET = {ADD, LIST, EDIT, DELETE, ACTION_POST, SHOW}
    """CRUD路由集合，{ADD, LIST, EDIT, DELETE, ACTION_POST, SHOW}"""
    RELATED_VIEW_SET = {ADD, LIST, EDIT, DELETE}
    """关联视图路由集合，{ADD, LIST, EDIT, DELETE}"""
    REST_MODEL_VIEW_CRUD_SET = {DELETE, GET, GET_LIST, POST, PUT, INFO}
    """REST 模型视图CRUD路由集合，{DELETE, GET, GET_LIST, POST, PUT, INFO}"""
    # endregion


MODEL_VIEW_RW_METHOD_PERMISSION_MAP = {
    "add": "write",
    "api": "read",
    "api_column_add": "write",
    "api_column_edit": "write",
    "api_create": "write",
    "api_delete": "write",
    "api_get": "read",
    "api_read": "read",
    "api_readvalues": "read",
    "api_update": "write",
    "annotation": "read",
    "delete": "write",
    "download": "read",
    "download_dashboards": "read",
    "edit": "write",
    "list": "read",
    "muldelete": "write",
    "mulexport": "read",
    "show": "read",
    "new": "write",
    "yaml_export": "read",
    "refresh": "write",
}
"""模型视图方法的读写权限字典，即方法和权限（write、read）的字典。"""

MODEL_API_RW_METHOD_PERMISSION_MAP = {
    "bulk_delete": "write",
    "delete": "write",
    "distinct": "read",
    "export": "read",
    "get": "read",
    "get_list": "read",
    "info": "read",
    "post": "write",
    "put": "write",
    "related": "read",
    "related_objects": "read",
    "schemas": "read",
    "select_star": "read",
    "table_metadata": "read",
    "test_connection": "read",
    "validate_parameters": "read",
    "favorite_status": "read",
    "thumbnail": "read",
    "import_": "write",
    "refresh": "write",
    "cache_screenshot": "read",
    "screenshot": "read",
    "data": "read",
    "data_from_cache": "read",
    "get_charts": "read",
    "get_datasets": "read",
    "function_names": "read",
    "available": "read",
    "get_data": "read",
}
"""模型API方法的读写权限字典。"""

EXTRA_FORM_DATA_APPEND_KEYS = {
    "adhoc_filters",
    "filters",
    "interactive_groupby",
    "interactive_highlight",
    "interactive_drilldown",
    "custom_form_data",
}
"""
额外表单数据追加键集合，可以基于这些键添加自定义数据到表单数据中。

adhoc_filters、filters、interactive_groupby、interactive_highlight、
interactive_drilldown、custom_form_data。
"""

EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS = {
    "granularity": "granularity",
    "granularity_sqla": "granularity",
    "time_column": "time_column",
    "time_grain": "time_grain",
    "time_range": "time_range",
    "druid_time_origin": "druid_time_origin",
    "time_grain_sqla": "time_grain_sqla",
    "time_range_endpoints": "time_range_endpoints",
}
"""额外表单数据重写覆盖常规字段映射字典，即自定义表单数据中的哪些键对应的要重写的常规表单数据字段名称。"""

EXTRA_FORM_DATA_OVERRIDE_EXTRA_KEYS = {
    "relative_start",
    "relative_end",
}
"""额外表单数据重写额外键集合，relative_start、relative_end。"""

EXTRA_FORM_DATA_OVERRIDE_KEYS = (
    set(EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS.values())
    | EXTRA_FORM_DATA_OVERRIDE_EXTRA_KEYS
)
"""额外表单数据重写键列表。"""


class PandasAxis(int, Enum):
    """Pandas坐标轴枚举，ROW，COLUMN。"""

    ROW = 0
    COLUMN = 1


class PandasPostprocessingCompare(str, Enum):
    """Pandas POST处理比较枚举，ABS、PCT、RAT。"""

    ABS = "absolute"
    PCT = "percentage"
    RAT = "ratio"


class CacheRegion(str, Enum):
    """缓存区域枚举，DEFAULT、DATA、THUMBNAIL。"""

    DEFAULT = "default"
    DATA = "data"
    THUMBNAIL = "thumbnail"
