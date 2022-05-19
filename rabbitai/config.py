# -*- coding: utf-8 -*-

"""
Rabbitai 的主配置文件。

在该文件中的所有配置都可以通过在该文件末尾由  ``from rabbitai_config import *``
导入 PYTHONPATH 目录下的 rabbitai_config 模块来重写。
"""

import imp
import importlib.util
import json
import logging
import os
import re
import sys
from collections import OrderedDict
from datetime import date, timedelta
from typing import Any, Callable, Dict, List, Optional, Type, TYPE_CHECKING, Union

from cachelib.base import BaseCache
from celery.schedules import crontab
from dateutil import tz
from flask import Blueprint
from flask_appbuilder.security.manager import AUTH_DB
# from pandas.io.parsers import STR_NA_VALUES
from pandas._libs.parsers import STR_NA_VALUES

from rabbitai.jinja_context import (  # pylint: disable=unused-import
    BaseTemplateProcessor,
)
from rabbitai.stats_logger import DummyStatsLogger
from rabbitai.typing import CacheConfig
from rabbitai.utils.core import is_test, parse_boolean_string
from rabbitai.utils.encrypt import SQLAlchemyUtilsAdapter
from rabbitai.utils.log import DBEventLogger
from rabbitai.utils.logging_configurator import DefaultLoggingConfigurator

# region Log

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from flask_appbuilder.security.sqla import models

    from rabbitai.connectors.sqla.models import (SqlaTable, )
    from rabbitai.models.core import Database

# 实时性能统计日志，StatsD 模块实现
STATS_LOGGER = DummyStatsLogger()
"""基于 StatsD 模块实现的性能统计日志记录器"""
EVENT_LOGGER = DBEventLogger()
"""数据库事件日志记录器"""

RABBITAI_LOG_VIEW = True
"""是否日志视图，默认True。"""

# endregion

# region dir

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
"""基目录，即该配置模块所在目录路径。"""

if "RABBITAI_HOME" in os.environ:
    DATA_DIR = os.environ["RABBITAI_HOME"]
    """数据目录，即由系统环境变量 RABBITAI_HOME 指定的目录。"""
else:
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".rabbitai")
    """数据目录，即用户家目录下的 .rabbitai 子目录。"""

# endregion

# region Rabbitai specific config

# region 版本

VERSION_INFO_FILE = os.path.join(BASE_DIR, "static", "version_info.json")
PACKAGE_JSON_FILE = os.path.join(BASE_DIR, "static", "assets", "package.json")


def _try_json_readversion(filepath: str) -> Optional[str]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f).get("version")
    except Exception:
        return None


def _try_json_readsha(filepath: str, length: int) -> Optional[str]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f).get("GIT_SHA")[:length]
    except Exception:
        return None


# version_info.json 可用或不可用，依赖于该配置加载的上下文，实际上是由安装程序 setup.py 生成的。
# 如果我们在运行RabbitAI，我们已经安装了，因此它已经存在。
# 可是，当进行单元测试时它不存在，所以我们读取 package.json
VERSION_STRING = _try_json_readversion(VERSION_INFO_FILE) or _try_json_readversion(
    PACKAGE_JSON_FILE
)

VERSION_SHA_LENGTH = 8
VERSION_SHA = _try_json_readsha(VERSION_INFO_FILE, VERSION_SHA_LENGTH)

# endregion

FAVICONS = [{"href": "/static/assets/images/favicon.png"}]
"""
网站图标，这里可以指定多个 favicon。 "href" 属性是必需的，但 "sizes," "type," 和 "rel" 是可选的。
例如:

```
{
    "href":path/to/image.png",
    "sizes": "16x16",
    "type": "image/png"
    "rel": "icon"
}
```

"""

DEFAULT_VIZ_TYPE = "table"
"""在图表浏览中使用的默认可视类型，table"""
ROW_LIMIT = 50000
"""行数限制，默认5万行。"""
VIZ_ROW_LIMIT = 10000
"""可视化时行数限制，默认1万行。"""

SAMPLES_ROW_LIMIT = 1000
"""在“浏览”视图中从数据源请求样本时检索的最大行数，默认1000行。"""

FILTER_SELECT_ROW_LIMIT = 10000
"""过滤器选择自动完成检索的最大行数，默认1万行。"""
RABBITAI_WORKERS = 2  # deprecated
RABBITAI_CELERY_WORKERS = 32  # deprecated

RABBITAI_WEBSERVER_PROTOCOL = "http"
"""Web服务器协议。"""
RABBITAI_WEBSERVER_ADDRESS = "0.0.0.0"
"""Web服务器地址。"""
RABBITAI_WEBSERVER_PORT = 8088
"""Web服务器端口号。"""

RABBITAI_WEBSERVER_TIMEOUT = int(timedelta(minutes=1).total_seconds())
"""
Web服务器超时。

这是一个重要的设置，应该低于[load balancer/proxy/envoy/kong/…]超时设置。
您还应该确保将WSGI服务器（gunicorn、nginx、apache等）超时设置配置为 <= 此设置
"""

RABBITAI_DASHBOARD_PERIODICAL_REFRESH_LIMIT = 0
"""当用户选择自动强制刷新频率时，仪表板周期强制刷新功能将使用这个设置"""
RABBITAI_DASHBOARD_PERIODICAL_REFRESH_WARNING_MESSAGE = None
"""仪表板周期强制刷新警告信息"""
RABBITAI_DASHBOARD_POSITION_DATA_LIMIT = 65535
"""仪表盘位置数据限制。"""
CUSTOM_SECURITY_MANAGER = None
"""自定义安全管理器。"""
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""是否让 SQLALCHEMY 跟踪修改。"""

SECRET_KEY = "\2\1thisismyscretkey\1\2\\e\\y\\y\\h"
"""秘钥"""

# endregion

# region SQLAlchemy 连接字符串。

# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, "rabbitai.db")
SQLALCHEMY_DATABASE_URI = 'postgresql://rabbitai:rabbitai@172.168.5.180:5432/rabbitaidb'
# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/rabbitaidb'
"""SQLAlchemy 连接字符串。"""

SQLALCHEMY_CUSTOM_PASSWORD_STORE = None
"""SQLAlchemy 自定义密码存储对象

为了为所有SQLACHEMY连接接通一个自定义密码存储，实现一个函数，该函数接受一个类型为 'sqla.engine.url' 的参数，
返回一个密码并设置SQLALCHEMY_CUSTOM_PASSWORD_STORE。

例如：

def lookup_password(url):
     return 'secret'
SQLALCHEMY_CUSTOM_PASSWORD_STORE = lookup_password

"""

SQLALCHEMY_ENCRYPTED_FIELD_TYPE_ADAPTER = SQLAlchemyUtilsAdapter
"""SQLAlchemy 加密字段适配器。
EncryptedFieldTypeAdapter在我们构建SqlAlchemy模型时使用，
该模型包括敏感字段，这些字段在发送到DB之前应该进行应用程序加密。
"""

# The limit of queries fetched for query search
QUERY_SEARCH_LIMIT = 1000
"""查询搜索限制，默认1000行。"""

# endregion

# region 网站相关

WTF_CSRF_ENABLED = True
"""Flask-WTF是否启用 CSRF """
WTF_CSRF_EXEMPT_LIST = ["rabbitai.views.core.log", "rabbitai.charts.api.data"]
"""添加需要免除CSRF保护的端点"""
DEBUG = os.environ.get("FLASK_ENV") == "development"
"""是否在调试模式下运行web服务器."""
FLASK_USE_RELOAD = True
"""Flask是否使用重载，默认True"""
SHOW_STACKTRACE = True
"""RabbitAI 允许在启用此功能时向用户显示服务器端python堆栈跟踪。这可能会带来安全隐患，在生产环境中关闭它更安全。"""

ENABLE_PROXY_FIX = False
"""当 ENABLE_PROXY_FIX 为 True 时，使用所有 X-Forwarded 标头。"""
PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 1, "x_prefix": 1}
"""当代理到不同端口时，设置 "x_port" 为 0 以避免避免下游问题。"""

# endregion

# region 关于 APP 构建者相关全局变量

APP_NAME = "RabbitAI"
"""应用程序名称。"""
APP_ICON = "/static/assets/images/rabbitai-logo-horiz.png"
"""应用图标文件路径。"""
APP_ICON_WIDTH = 126
"""应用图标宽度。"""
LOGO_TARGET_PATH = None
"""指定单击徽标会将用户带到的位置。例如：设置 '/' 导航到'/rabbitai/welcome/'。"""
LOGO_TOOLTIP = ""
"""指定将鼠标悬停在应用程序图标/徽标上时应显示的工具提示"""

LOGO_RIGHT_TEXT: Union[Callable[[], str], str] = ""
"""指定应显示在徽标右侧的任何文本"""

FAB_API_SWAGGER_UI = True
"""为rabbitai openapi规范启用SWAGGER UI,ex: http://localhost:8080/swagger/v1"""

# endregion

# region Druid

"""
什么是druid

    druid是一个为OLAP查询需求而设计的开源大数据系统，druid提供低延时的数据插入，实时的数据查询druid使用Java开发，
    基于Jetty提供http rest服务，也提供了Java/Python等语言的工具包druid是一个集群系统，使用zookeeper做节点管理和事件监控

druid的特点

    druid的核心是时间序列，把数据按照时间序列分批存储，十分适合用于对按时间进行统计分析的场景，druid把数据列分为三类：
    时间戳、维度列、指标列druid不支持多表Join，druid中的数据一般是使用其他计算框架(Spark等)预计算好的低层次统计数据druid执行其擅长的查询类型时，
    从数十亿条记录中过滤、汇聚只有亚秒级延迟druid支持水平扩展，
    查询节点越多、所支持的查询数据量越大、响应越快druid完美支持的查询类型比较简单，查询场景限制较多，
    一些常用的SQL(groupby等)语句在druid里运行速度一般druid支持低延时的数据插入，数据实时可查，不支持行级别的数据更新

druid为什么快

    druid在数据插入时按照时间序列将数据分为若干segment，支持低延时地按照时间序列上卷，所以按时间做聚合效率很高druid数据按列存储，
    每个维度列都建立索引，所以按列过滤取值效率很高druid用以查询的Broker和Historical支持多级缓存，每个segment启动一个线程并发执行查询，
    查询支持多Historical内部的线程级并发及Historical之间的进程间并发，Broker将各Historical的查询结果做合并

druid的高可用性

    MetaStore挂掉：无法感知新的Segment生成，不影响老数据
    Indexing Service挂掉：无法执行新的任务，新数据无法摄入，不影响查询
    Broker挂掉：本Broker节点不能查询，其他节点Broker继续服务，不影响数据摄入
    Historical挂掉：Coordinator Node重分配该节点上segment到其它节点
    Coordinator挂掉：Segment不会被加载和删除，选举新leader
    Zookeeper挂掉：无法执行新的任务，新数据进不来；Broker有缓存
    
"""

DRUID_TZ = tz.tzutc()
"""Druid查询时区

- tz.tzutc() : 使用 utc 时区
- tz.tzlocal() : 使用本地时区
- tz.gettz('Asia/Shanghai') : 使用指定名称的时区
"""

DRUID_ANALYSIS_TYPES = ["cardinality"]

DRUID_IS_ACTIVE = False
"""旧式Druid NoSQL（原生）连接器 Druid 在其较新版本中支持SQL接口。
将此标志设置为True将启用不推荐使用的基于API的Druid连接器。此功能可能会在将来删除。"""

DRUID_METADATA_LINKS_ENABLED = True
"""如果Druid处于活动状态，是否包含扫描/刷新Druid数据源的链接。如果您试图断开与Druid NoSQL连接器的连接，则应禁用此选项。"""

# endregion

# region AUTHENTICATION CONFIG
# ----------------------------------------------------
AUTH_TYPE = AUTH_DB
"""授权类型，支持：AUTH_OID、AUTH_DB、AUTH_LDAP、AUTH_REMOTE_USER"""
# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'
"""设置完整管理员角色名"""
# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'
"""公共角色名称，不需要认证"""
# Will allow user self registration
# AUTH_USER_REGISTRATION = True
"""是否允许注册用户"""
# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"
"""默认用户注册角色"""
# When using LDAP Auth, setup the LDAP server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"
"""LDAP 服务器地址"""
# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://open.login.yahoo.com/' },
#    { 'name': 'Flickr', 'url': 'https://www.flickr.com/<username>' },
"""OpenID 提供者"""
# ---------------------------------------------------
# Roles config
# ---------------------------------------------------
PUBLIC_ROLE_LIKE: Optional[str] = None
"""为公共角色授予与所选内置角色相同的权限集。如果希望匿名用户能够查看仪表盘，这将非常有用。仍然需要对特定数据集进行显式授权。"""

# endregion

# region Babel 配置

# 设置默认语言代码
BABEL_DEFAULT_LOCALE = "zh"
# 存储翻译文件的路径
BABEL_DEFAULT_FOLDER = "rabbitai/translations"
# 应用允许的翻译
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "es": {"flag": "es", "name": "Spanish"},
    "it": {"flag": "it", "name": "Italian"},
    "fr": {"flag": "fr", "name": "French"},
    "zh": {"flag": "cn", "name": "Chinese"},
    "ja": {"flag": "jp", "name": "Japanese"},
    "de": {"flag": "de", "name": "German"},
    "pt": {"flag": "pt", "name": "Portuguese"},
    "pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
    "ru": {"flag": "ru", "name": "Russian"},
    "ko": {"flag": "kr", "name": "Korean"},
    "sl": {"flag": "si", "name": "Slovenian"},
}

# endregion

# region Feature flags
# ---------------------------------------------------
# 默认功能标志（Feature flags）。
# 这些值可以通过 rabbitai_config.py 中的 FEATURE_FLAGS 字段重写。
# 例如, DEFAULT_FEATURE_FLAGS = { 'FOO': True, 'BAR': False }，
# 在 rabbitai_config.py 中 FEATURE_FLAGS = { 'BAR': True, 'BAZ': True }，
# 那么组合后为 { 'FOO': True, 'BAR': True, 'BAZ': True }
DEFAULT_FEATURE_FLAGS: Dict[str, bool] = {
    # 允许仪表盘使用子域名发送请求，对于每个域名也需要 ENABLE_CORS 和 RABBITAI_WEBSERVER_DOMAINS
    "ALLOW_DASHBOARD_DOMAIN_SHARDING": True,
    # 是否引入客户端（浏览器）缓存的实验性功能
    "CLIENT_CACHE": False,
    "DISABLE_DATASET_SOURCE_EDIT": False,
    "DYNAMIC_PLUGINS": False,
    # 出于某些安全考虑，可能需要对 explore_json 端点的所有查询请求实施CSRF保护。
    # 在 RabbitAI 中，对所有 POST 请求我们使用 `flask-csrf <https://sjl.bitbucket.io/flask-csrf/>`_ 添加CSRF保护，
    # 但是，这种保护不能用于 GET 方法。
    # 当 ENABLE_EXPLORE_JSON_CSRF_PROTECTION 设置为 true 时，用户不能对 explore_json 发送 GET请求。
    # explore_json 接受 GET 和 POST 请求。
    # 详见： `PR 7935 <https://github.com/apache/rabbitai/pull/7935>`_
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": False,
    "ENABLE_TEMPLATE_PROCESSING": False,
    "ENABLE_TEMPLATE_REMOVE_FILTERS": False,
    "KV_STORE": False,
    # 当启用该标志时，Presto 中的嵌套类型将展开到额外列/数组。
    # 这是实验性的，并不适用于所有嵌套类型。
    "PRESTO_EXPAND_DATA": False,
    # 是否公开API端点以计算缩略图
    "THUMBNAILS": False,
    "DASHBOARD_CACHE": False,
    "REMOVE_SLICE_LEVEL_LABEL_COLORS": False,
    "SHARE_QUERIES_VIA_KV_STORE": False,
    "TAGGING_SYSTEM": False,
    "SQLLAB_BACKEND_PERSISTENCE": False,
    "LISTVIEWS_DEFAULT_CARD_VIEW": False,
    # 是否启用 React 视图替换 FAB 视图 (list, edit, show)。
    # 这是一项正在进行的工作，因此并非FAB中的所有可用功能都已实现。
    "ENABLE_REACT_CRUD_VIEWS": True,
    # 如果为True，则此标志允许在 Markdown 组件中显示HTML标记
    "DISPLAY_MARKDOWN_HTML": True,
    # 如果为True，则在 Markdown 组件中转义HTML（而不是呈现它）
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_NATIVE_FILTERS": False,
    "DASHBOARD_CROSS_FILTERS": False,
    "DASHBOARD_NATIVE_FILTERS_SET": False,
    "DASHBOARD_FILTERS_EXPERIMENTAL": False,
    "GLOBAL_ASYNC_QUERIES": False,
    "VERSIONED_EXPORT": False,
    # Note that: RowLevelSecurityFilter is only given by default to the Admin role
    # and the Admin Role does have the all_datasources security permission.
    # But, if users create a specific role with access to RowLevelSecurityFilter MVC
    # and a custom datasource access, the table dropdown will not be correctly filtered
    # by that custom datasource access. So we are assuming a default security config,
    # a custom security config could potentially give access to setting filters on
    # tables that users do not have access to.
    "ROW_LEVEL_SECURITY": True,
    # 是否启用更改提示和报告
    "ALERT_REPORTS": False,
    # 启用实验功能以搜索其他仪表板
    "OMNIBAR": False,
    "DASHBOARD_RBAC": False,
    "ENABLE_EXPLORE_DRAG_AND_DROP": False,
    # 启用 ALERTS_ATTACH_REPORTS 后，系统会发送电子邮件和带有屏幕截图和链接的松弛消息，
    # 禁用 ALERTS_ATTACH_REPORTS 时，系统不生成屏幕截图
    # 对于 'alert' 类型报告，发送发送电子邮件和带有链接的松弛消息;
    # 对于 'report' 类型报告，发送电子邮件和带有屏幕截图和链接的松弛消息
    "ALERTS_ATTACH_REPORTS": True,
    # FORCE_DATABASE_CONNECTIONS_SSL 已弃用
    "FORCE_DATABASE_CONNECTIONS_SSL": False,
    # 启用 ENFORCE_DB_ENCRYPTION_UI 强制所有数据库连接在存储数据时进行加密。
    "ENFORCE_DB_ENCRYPTION_UI": False,
    # 允许用户导出表格viz类型的完整CSV。
    # 这可能会导致服务器内存或计算量不足。
    "ALLOW_FULL_CSV_EXPORT": False,
    "UX_BETA": False,
}

# 功能标志也可以通过 'RABBITAI_FEATURE_' 前缀的环境变量设置。
DEFAULT_FEATURE_FLAGS.update(
    {
        k[len("RABBITAI_FEATURE_"):]: parse_boolean_string(v)
        for k, v in os.environ.items()
        if re.search(r"^RABBITAI_FEATURE_\w+", k)
    }
)

# 功能标志
FEATURE_FLAGS: Dict[str, bool] = {}

# 接收所有特征标志的dict的函数(DEFAULT_FEATURE_FLAGS 与 FEATURE_FLAGS合并)
# Note the dict of feature flags passed to the function is a deepcopy of the dict in the config,
# and can therefore be mutated without side-effect
#
# GET_FEATURE_FLAGS_FUNC can be used to implement progressive rollouts,
# role-based features, or a full on A/B testing framework.
#
# from flask import g, request
# def GET_FEATURE_FLAGS_FUNC(feature_flags_dict: Dict[str, bool]) -> Dict[str, bool]:
#     if hasattr(g, "user") and g.user.is_active:
#         feature_flags_dict['some_feature'] = g.user and g.user.get_id() == 5
#     return feature_flags_dict
GET_FEATURE_FLAGS_FUNC: Optional[Callable[[Dict[str, bool]], Dict[str, bool]]] = None
# endregion

# region Schemes

# EXTRA_CATEGORICAL_COLOR_SCHEMES is used for adding custom categorical color schemes
# example code for "My custom warm to hot" color scheme
# EXTRA_CATEGORICAL_COLOR_SCHEMES = [
#     {
#         "id": 'myVisualizationColors',
#         "description": '',
#         "label": 'My Visualization Colors',
#         "colors":
#          ['#006699', '#009DD9', '#5AAA46', '#44AAAA', '#DDAA77', '#7799BB', '#88AA77',
#          '#552288', '#5AAA46', '#CC7788', '#EEDD55', '#9977BB', '#BBAA44', '#DDCCDD']
#     }]
EXTRA_CATEGORICAL_COLOR_SCHEMES: List[Dict[str, Any]] = []

# THEME_OVERRIDES is used for adding custom theme to RabbitAI
# example code for "My theme" custom scheme
# THEME_OVERRIDES = {
#   "borderRadius": 4,
#   "colors": {
#     "primary": {
#       "base": 'red',
#     },
#     "secondary": {
#       "base": 'green',
#     },
#     "grayscale": {
#       "base": 'orange',
#     }
#   }
# }
THEME_OVERRIDES: Dict[str, Any] = {}

# EXTRA_SEQUENTIAL_COLOR_SCHEMES is used for adding custom sequential color schemes
# EXTRA_SEQUENTIAL_COLOR_SCHEMES =  [
#     {
#         "id": 'warmToHot',
#         "description": '',
#         "isDiverging": True,
#         "label": 'My custom warm to hot',
#         "colors":
#          ['#552288', '#5AAA46', '#CC7788', '#EEDD55', '#9977BB', '#BBAA44', '#DDCCDD',
#          '#006699', '#009DD9', '#5AAA46', '#44AAAA', '#DDAA77', '#7799BB', '#88AA77']
#     }]
EXTRA_SEQUENTIAL_COLOR_SCHEMES: List[Dict[str, Any]] = []

# endregion

# region Thumbnail config (behind feature flag)
# Also used by Alerts & Reports
# ---------------------------------------------------
THUMBNAIL_SELENIUM_USER = "admin"
THUMBNAIL_CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "null", "CACHE_NO_NULL_WARNING": True}

# Time before selenium times out after trying to locate an element on the page and wait
# for that element to load for a screenshot.
SCREENSHOT_LOCATE_WAIT = int(timedelta(seconds=10).total_seconds())
# Time before selenium times out after waiting for all DOM class elements named
# "loading" are gone.
SCREENSHOT_LOAD_WAIT = int(timedelta(minutes=1).total_seconds())
# Selenium destroy retries
SCREENSHOT_SELENIUM_RETRIES = 5
# Give selenium an headstart, in seconds
SCREENSHOT_SELENIUM_HEADSTART = 3
# Wait for the chart animation, in seconds
SCREENSHOT_SELENIUM_ANIMATION_WAIT = 5

# endregion

# region Image and file configuration
# ---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = BASE_DIR + "/app/static/uploads/"
UPLOAD_CHUNK_SIZE = 4096

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = BASE_DIR + "/app/static/uploads/"

# The image upload url, when using models with images
IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)

# endregion

# region cache

# 默认缓存超时，适用于所有缓存后端，除非在每个缓存配置中特别重写。
CACHE_DEFAULT_TIMEOUT = int(timedelta(days=1).total_seconds())

# RabbitAI 的默认缓存配置
CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "null", "CACHE_NO_NULL_WARNING": True}

# 数据源元数据和查询结果的缓存
DATA_CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "null", "CACHE_NO_NULL_WARNING": True}

# 按数据源UID（通过CacheKey）存储缓存键，以进行自定义处理/失效
STORE_CACHE_KEYS_IN_METADATA_DB = False

# endregion

# CORS 选项
ENABLE_CORS = False
CORS_OPTIONS: Dict[Any, Any] = {}

# Chrome 允许每个域名同时打开6个连接，当仪表盘中有超过 6 各切片时，
# 很多时间提取请求排队等待下一个可用套接字。
# PR#5039正试图允许 RabbitAI 域名共享，
# 此标志仅通过配置启用（默认情况下，RabbitAI不允许跨域请求）。
RABBITAI_WEBSERVER_DOMAINS = None

# 允许上传到仪表盘视图的文件格式
EXCEL_EXTENSIONS = {"xlsx", "xls"}
CSV_EXTENSIONS = {"csv", "tsv", "txt"}
ALLOWED_EXTENSIONS = {*EXCEL_EXTENSIONS, *CSV_EXTENSIONS}

# CSV 选项: 将作为参数传递到 DataFrame.to_csv 方法的 key/value 对。
CSV_EXPORT = {"encoding": "utf-8"}

# region 时间粒度配置
# ---------------------------------------------------
# 应用程序中要禁用的时间粒度列表 (详见 rabbitai/db_engine_specs.builtin_time_grains 中定义的时间粒度)。
# 例如: 要禁用 1 秒时间粒度：
# TIME_GRAIN_DENYLIST = ['PT1S']
TIME_GRAIN_DENYLIST: List[str] = []

# Additional time grains to be supported using similar definitions as in
# rabbitai/db_engine_specs.builtin_time_grains.
# For example: To add a new 2 second time grain:
# TIME_GRAIN_ADDONS = {'PT2S': '2 second'}
TIME_GRAIN_ADDONS: Dict[str, str] = {}

# Implementation of additional time grains per engine.
# The column to be truncated is denoted `{col}` in the expression.
# For example: To implement 2 second time grain on clickhouse engine:
# TIME_GRAIN_ADDON_EXPRESSIONS = {
#     'clickhouse': {
#         'PT2S': 'toDateTime(intDiv(toUInt32(toDateTime({col})), 2)*2)'
#     }
# }
TIME_GRAIN_ADDON_EXPRESSIONS: Dict[str, Dict[str, str]] = {}

# endregion

VIZ_TYPE_DENYLIST: List[str] = []
"""环境中不允许的 viz_types 列表，例如：禁用透视表和地图树：VIZ_TYPE_DENYLIST = ['pivot_table', 'treemap']"""
DRUID_DATA_SOURCE_DENYLIST: List[str] = []
"""druid集群中不允许的数据源列表"""

# region Modules, datasources and middleware to be registered

DEFAULT_MODULE_DS_MAP = OrderedDict(
    [
        ("rabbitai.connectors.sqla.models", ["SqlaTable"]),
        ("rabbitai.connectors.druid.models", ["DruidDatasource"]),
    ]
)
ADDITIONAL_MODULE_DS_MAP: Dict[str, List[str]] = {}
ADDITIONAL_MIDDLEWARE: List[Callable[..., Any]] = []

# endregion

# region Log

# 1) https://docs.python-guide.org/writing/logging/
# 2) https://docs.python.org/2/library/logging.config.html

# Default configurator will consume the LOG_* settings below
LOGGING_CONFIGURATOR = DefaultLoggingConfigurator()

# Console Log Settings

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
LOG_LEVEL = "DEBUG"

# ---------------------------------------------------
# Enable Time Rotate Log Handler
# ---------------------------------------------------
# LOG_LEVEL = DEBUG, INFO, WARNING, ERROR, CRITICAL

ENABLE_TIME_ROTATE = False
TIME_ROTATE_LOG_LEVEL = "DEBUG"
FILENAME = os.path.join(DATA_DIR, "rabbitai.log")
ROLLOVER = "midnight"
INTERVAL = 1
BACKUP_COUNT = 30

# Custom logger for auditing queries. This can be used to send ran queries to a
# structured immutable store for auditing purposes. The function is called for
# every query ran, in both SQL Lab and charts/dashboards.
# def QUERY_LOGGER(
#     database,
#     query,
#     schema=None,
#     user=None,
#     client=None,
#     security_manager=None,
#     log_params=None,
# ):
#     pass
QUERY_LOGGER = None

# endregion

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")

# region celery config

# Default celery config is to use SQLA as a broker, in a production setting
# you'll want to use a proper broker as specified here:
# http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html


class CeleryConfig:
    BROKER_URL = "sqla+sqlite:///celerydb.sqlite"
    CELERY_IMPORTS = ("rabbitai.sql_lab", "rabbitai.tasks")
    CELERY_RESULT_BACKEND = "db+sqlite:///celery_results.sqlite"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERY_ANNOTATIONS = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": int(timedelta(seconds=120).total_seconds()),
            "soft_time_limit": int(timedelta(seconds=150).total_seconds()),
            "ignore_result": True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        },
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# Set celery config to None to disable all the above configuration
# CELERY_CONFIG = None

# endregion

# Additional static HTTP headers to be served by your RabbitAI server. Note
# Flask-Talisman applies the relevant security HTTP headers.
#
# DEFAULT_HTTP_HEADERS: sets default values for HTTP headers. These may be overridden
# within the app
# OVERRIDE_HTTP_HEADERS: sets override values for HTTP headers. These values will
# override anything set within the app
DEFAULT_HTTP_HEADERS: Dict[str, Any] = {}
OVERRIDE_HTTP_HEADERS: Dict[str, Any] = {}
HTTP_HEADERS: Dict[str, Any] = {}

# region SQL Lab

# Maximum number of rows returned from a database
# in async mode, no more than SQL_MAX_ROW will be returned and stored
# in the results backend. This also becomes the limit when exporting CSVs
SQL_MAX_ROW = 100000

# Maximum number of rows displayed in SQL Lab UI
# Is set to avoid out of memory/localstorage issues in browsers. Does not affect
# exported CSVs
DISPLAY_MAX_ROW = 10000

# Default row limit for SQL Lab queries. Is overridden by setting a new limit in
# the SQL Lab UI
DEFAULT_SQLLAB_LIMIT = 1000

# Maximum number of tables/views displayed in the dropdown window in SQL Lab.
MAX_TABLE_NAMES = 3000

# Adds a warning message on sqllab save query and schedule query modals.
SQLLAB_SAVE_WARNING_MESSAGE = None
SQLLAB_SCHEDULE_WARNING_MESSAGE = None

# The db id here results in selecting this one as a default in SQL Lab
DEFAULT_DB_ID = None

# Timeout duration for SQL Lab synchronous queries
SQLLAB_TIMEOUT = int(timedelta(seconds=30).total_seconds())

# Timeout duration for SQL Lab query validation
SQLLAB_VALIDATION_TIMEOUT = int(timedelta(seconds=10).total_seconds())

# SQLLAB_DEFAULT_DBID
SQLLAB_DEFAULT_DBID = None

# The MAX duration a query can run for before being killed by celery.
SQLLAB_ASYNC_TIME_LIMIT_SEC = int(timedelta(hours=6).total_seconds())

# Some databases support running EXPLAIN queries that allow users to estimate
# query costs before they run. These EXPLAIN queries should have a small
# timeout.
SQLLAB_QUERY_COST_ESTIMATE_TIMEOUT = int(timedelta(seconds=10).total_seconds())
# The feature is off by default, and currently only supported in Presto and Postgres.
# It also need to be enabled on a per-database basis, by adding the key/value pair
# `cost_estimate_enabled: true` to the database `extra` attribute.
ESTIMATE_QUERY_COST = False
# The cost returned by the databases is a relative value; in order to map the cost to
# a tangible value you need to define a custom formatter that takes into consideration
# your specific infrastructure. For example, you could analyze queries a posteriori by
# running EXPLAIN on them, and compute a histogram of relative costs to present the
# cost as a percentile:
#
# def postgres_query_cost_formatter(
#     result: List[Dict[str, Any]]
# ) -> List[Dict[str, str]]:
#     # 25, 50, 75% percentiles
#     percentile_costs = [100.0, 1000.0, 10000.0]
#
#     out = []
#     for row in result:
#         relative_cost = row["Total cost"]
#         percentile = bisect.bisect_left(percentile_costs, relative_cost) + 1
#         out.append({
#             "Relative cost": relative_cost,
#             "Percentile": str(percentile * 25) + "%",
#         })
#
#     return out
#
# FEATURE_FLAGS = {
#     "ESTIMATE_QUERY_COST": True,
#     "QUERY_COST_FORMATTERS_BY_ENGINE": {"postgresql": postgres_query_cost_formatter},
# }

# Flag that controls if limit should be enforced on the CTA (create table as queries).
SQLLAB_CTAS_NO_LIMIT = False

# This allows you to define custom logic around the "CREATE TABLE AS" or CTAS feature
# in SQL Lab that defines where the target schema should be for a given user.
# Database `CTAS Schema` has a precedence over this setting.
# Example below returns a username and CTA queries will write tables into the schema
# name `username`
# SQLLAB_CTAS_SCHEMA_NAME_FUNC = lambda database, user, schema, sql: user.username
# This is move involved example where depending on the database you can leverage data
# available to assign schema for the CTA query:
# def compute_schema_name(database: Database, user: User, schema: str, sql: str) -> str:
#     if database.name == 'mysql_payments_slave':
#         return 'tmp_rabbitai_schema'
#     if database.name == 'presto_gold':
#         return user.username
#     if database.name == 'analytics':
#         if 'analytics' in [r.name for r in user.roles]:
#             return 'analytics_cta'
#         else:
#             return f'tmp_{schema}'
# Function accepts database object, user object, schema name and sql that will be run.
SQLLAB_CTAS_SCHEMA_NAME_FUNC: Optional[
    Callable[["Database", "models.User", str, str], str]
] = None

# If enabled, it can be used to store the results of long-running queries
# in SQL Lab by using the "Run Async" button/feature
RESULTS_BACKEND: Optional[BaseCache] = None

# Use PyArrow and MessagePack for async query results serialization,
# rather than JSON. This feature requires additional testing from the
# community before it is fully adopted, so this config option is provided
# in order to disable should breaking issues be discovered.
RESULTS_BACKEND_USE_MSGPACK = True

# The S3 bucket where you want to store your external hive tables created
# from CSV files. For example, 'companyname-rabbitai'
CSV_TO_HIVE_UPLOAD_S3_BUCKET = None

# The directory within the bucket specified above that will
# contain all the external tables
CSV_TO_HIVE_UPLOAD_DIRECTORY = "EXTERNAL_HIVE_TABLES/"


# Function that creates upload directory dynamically based on the
# database used, user and schema provided.
def CSV_TO_HIVE_UPLOAD_DIRECTORY_FUNC(
    database: "Database",
    user: "models.User",  # pylint: disable=unused-argument
    schema: Optional[str],
) -> str:
    # Note the final empty path enforces a trailing slash.
    return os.path.join(
        CSV_TO_HIVE_UPLOAD_DIRECTORY, str(database.id), schema or "", ""
    )


# The namespace within hive where the tables created from
# uploading CSVs will be stored.
UPLOADED_CSV_HIVE_NAMESPACE: Optional[str] = None

# Function that computes the allowed schemas for the CSV uploads.
# Allowed schemas will be a union of schemas_allowed_for_csv_upload
# db configuration and a result of this function.

# mypy doesn't catch that if case ensures list content being always str
ALLOWED_USER_CSV_SCHEMA_FUNC: Callable[["Database", "models.User"], List[str]] = (
    lambda database, user: [UPLOADED_CSV_HIVE_NAMESPACE]
    if UPLOADED_CSV_HIVE_NAMESPACE
    else []
)

# Values that should be treated as nulls for the csv uploads.
CSV_DEFAULT_NA_NAMES = list(STR_NA_VALUES)

# A dictionary of items that gets merged into the Jinja context for
# SQL Lab. The existing context gets updated with this dictionary,
# meaning values for existing keys get overwritten by the content of this
# dictionary. Exposing functionality through JINJA_CONTEXT_ADDONS has security
# implications as it opens a window for a user to execute untrusted code.
# It's important to make sure that the objects exposed (as well as objects attached
# to those objets) are harmless. We recommend only exposing simple/pure functions that
# return native types.
JINJA_CONTEXT_ADDONS: Dict[str, Callable[..., Any]] = {}

# A dictionary of macro template processors (by engine) that gets merged into global
# template processors. The existing template processors get updated with this
# dictionary, which means the existing keys get overwritten by the content of this
# dictionary. The customized addons don't necessarily need to use Jinja templating
# language. This allows you to define custom logic to process templates on a per-engine
# basis. Example value = `{"presto": CustomPrestoTemplateProcessor}`
CUSTOM_TEMPLATE_PROCESSORS: Dict[str, Type[BaseTemplateProcessor]] = {}

# endregion

# 由API/RabbitAI控制且不应由人类更改的角色。
ROBOT_PERMISSION_ROLES = ["Public", "Gamma", "Alpha", "Admin", "sql_lab"]

CONFIG_PATH_ENV_VAR = "RABBITAI_CONFIG_PATH"

# 如果指定了callable，则会在应用程序启动时调用它，同时将引用传递给Flask应用程序。
# 这可以用于以任何方式更改Flask应用程序。
# example: FLASK_APP_MUTATOR = lambda x: x.before_request = f
FLASK_APP_MUTATOR = None

# Set this to false if you don't want users to be able to request/grant
# datasource access requests from/to other users.
ENABLE_ACCESS_REQUEST = False

# region smtp server configuration
EMAIL_NOTIFICATIONS = False
SMTP_HOST = "localhost"
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "rabbitai"
SMTP_PORT = 25
SMTP_PASSWORD = "rabbitai"
SMTP_MAIL_FROM = "pengsongbo@hotmail.com"
# endregion

ENABLE_CHUNK_ENCODING = False

# region FAB

# Whether to bump the logging level to ERROR on the flask_appbuilder package
# Set to False if/when debugging FAB related issues like
# permission management
SILENCE_FAB = True

FAB_ADD_SECURITY_VIEWS = True
FAB_ADD_SECURITY_PERMISSION_VIEW = False
FAB_ADD_SECURITY_VIEW_MENU_VIEW = False
FAB_ADD_SECURITY_PERMISSION_VIEWS_VIEW = False

# endregion

# The link to a page containing common errors and their resolutions
# It will be appended at the bottom of sql_lab errors.
TROUBLESHOOTING_LINK = ""

# CSRF token timeout, set to None for a token that never expires
WTF_CSRF_TIME_LIMIT = int(timedelta(weeks=1).total_seconds())

# This link should lead to a page with instructions on how to gain access to a
# Datasource. It will be placed at the bottom of permissions errors.
PERMISSION_INSTRUCTIONS_LINK = ""

# Integrate external Blueprints to the app by passing them to your
# configuration. These blueprints will get integrated in the app
BLUEPRINTS: List[Blueprint] = []

# Provide a callable that receives a tracking_url and returns another
# URL. This is used to translate internal Hadoop job tracker URL
# into a proxied one
TRACKING_URL_TRANSFORMER = lambda x: x

# Interval between consecutive polls when using Hive Engine
HIVE_POLL_INTERVAL = int(timedelta(seconds=5).total_seconds())

# Interval between consecutive polls when using Presto Engine
# See here: https://github.com/dropbox/PyHive/blob/8eb0aeab8ca300f3024655419b93dad926c1a351/pyhive/presto.py#L93
PRESTO_POLL_INTERVAL = int(timedelta(seconds=1).total_seconds())

# Allow for javascript controls components
# this enables programmers to customize certain charts (like the
# geospatial ones) by inputing javascript in controls. This exposes
# an XSS security vulnerability
ENABLE_JAVASCRIPT_CONTROLS = False

# The id of a template dashboard that should be copied to every new user
DASHBOARD_TEMPLATE_ID = None

# A callable that allows altering the database connection URL and params
# on the fly, at runtime. This allows for things like impersonation or
# arbitrary logic. For instance you can wire different users to
# use different connection parameters, or pass their email address as the
# username. The function receives the connection uri object, connection
# params, the username, and returns the mutated uri and params objects.
# Example:
#   def DB_CONNECTION_MUTATOR(uri, params, username, security_manager, source):
#       user = security_manager.find_user(username=username)
#       if user and user.email:
#           uri.username = user.email
#       return uri, params
#
# Note that the returned uri and params are passed directly to sqlalchemy's
# as such `create_engine(url, **params)`
DB_CONNECTION_MUTATOR = None

# A function that intercepts the SQL to be executed and can alter it.
# The use case is can be around adding some sort of comment header
# with information such as the username and worker node information
#
#    def SQL_QUERY_MUTATOR(sql, user_name, security_manager, database):
#        dttm = datetime.now().isoformat()
#        return f"-- [SQL LAB] {username} {dttm}\n{sql}"
SQL_QUERY_MUTATOR = None

# Enable / disable scheduled email reports
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
ENABLE_SCHEDULED_EMAIL_REPORTS = False

# Enable / disable Alerts, where users can define custom SQL that
# will send emails with screenshots of charts or dashboards periodically
# if it meets the criteria
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
ENABLE_ALERTS = False

# ---------------------------------------------------
# Alerts & Reports
# ---------------------------------------------------
# Used for Alerts/Reports (Feature flask ALERT_REPORTS) to set the size for the
# sliding cron window size, should be synced with the celery beat config minus 1 second
ALERT_REPORTS_CRON_WINDOW_SIZE = 59
ALERT_REPORTS_WORKING_TIME_OUT_KILL = True
# if ALERT_REPORTS_WORKING_TIME_OUT_KILL is True, set a celery hard timeout
# Equal to working timeout + ALERT_REPORTS_WORKING_TIME_OUT_LAG
ALERT_REPORTS_WORKING_TIME_OUT_LAG = int(timedelta(seconds=10).total_seconds())
# if ALERT_REPORTS_WORKING_TIME_OUT_KILL is True, set a celery hard timeout
# Equal to working timeout + ALERT_REPORTS_WORKING_SOFT_TIME_OUT_LAG
ALERT_REPORTS_WORKING_SOFT_TIME_OUT_LAG = int(timedelta(seconds=1).total_seconds())
# If set to true no notification is sent, the worker will just log a message.
# Useful for debugging
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

# A custom prefix to use on all Alerts & Reports emails
EMAIL_REPORTS_SUBJECT_PREFIX = "[Report] "

# Slack API token for the rabbitai reports, either string or callable
SLACK_API_TOKEN: Optional[Union[Callable[[], str], str]] = None
SLACK_PROXY = None

# If enabled, certain features are run in debug mode
# Current list:
# * Emails are sent using dry-run mode (logging only)
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
SCHEDULED_EMAIL_DEBUG_MODE = False

# This auth provider is used by background (offline) tasks that need to access
# protected resources. Can be overridden by end users in order to support
# custom auth mechanisms
MACHINE_AUTH_PROVIDER_CLASS = "rabbitai.utils.machine_auth.MachineAuthProvider"

# Email reports - minimum time resolution (in minutes) for the crontab
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
EMAIL_REPORTS_CRON_RESOLUTION = 15

# The MAX duration (in seconds) a email schedule can run for before being killed
# by celery.
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
EMAIL_ASYNC_TIME_LIMIT_SEC = int(timedelta(minutes=5).total_seconds())

# Send bcc of all reports to this address. Set to None to disable.
# This is useful for maintaining an audit trail of all email deliveries.
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
EMAIL_REPORT_BCC_ADDRESS = None

# User credentials to use for generating reports
# This user should have permissions to browse all the dashboards and
# slices.
# TODO: In the future, login as the owner of the item to generate reports
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
EMAIL_REPORTS_USER = "admin"

# The webdriver to use for generating reports. Use one of the following
# firefox
#   Requires: geckodriver and firefox installations
#   Limitations: can be buggy at times
# chrome:
#   Requires: headless chrome
#   Limitations: unable to generate screenshots of elements
WEBDRIVER_TYPE = "firefox"

# Window size - this will impact the rendering of the data
WEBDRIVER_WINDOW = {"dashboard": (1600, 2000), "slice": (3000, 1200)}

# An optional override to the default auth hook used to provide auth to the
# offline webdriver
WEBDRIVER_AUTH_FUNC = None

# Any config options to be passed as-is to the webdriver
WEBDRIVER_CONFIGURATION: Dict[Any, Any] = {"service_log_path": "/dev/null"}

# Additional args to be passed as arguments to the config object
# Note: these options are Chrome-specific. For FF, these should
# only include the "--headless" arg
WEBDRIVER_OPTION_ARGS = ["--headless", "--marionette"]

# The base URL to query for accessing the user interface
WEBDRIVER_BASEURL = "http://0.0.0.0:8080/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
# Time selenium will wait for the page to load and render for the email report.
EMAIL_PAGE_RENDER_WAIT = int(timedelta(seconds=30).total_seconds())

# Send user to a link where they can report bugs
BUG_REPORT_URL = None

# Send user to a link where they can read more about Rabbitai
DOCUMENTATION_URL = None
DOCUMENTATION_TEXT = "Documentation"
DOCUMENTATION_ICON = None  # Recommended size: 16x16

# What is the Last N days relative in the time selector to:
# 'today' means it is midnight (00:00:00) in the local timezone
# 'now' means it is relative to the query issue time
# If both start and end time is set to now, this will make the time
# filter a moving window. By only setting the end time to now,
# start time will be set to midnight, while end will be relative to
# the query issue time.
DEFAULT_RELATIVE_START_TIME = "today"
DEFAULT_RELATIVE_END_TIME = "today"

# Configure which SQL validator to use for each engine
SQL_VALIDATORS_BY_ENGINE = {
    "presto": "PrestoDBSQLValidator",
    "postgresql": "PostgreSQLValidator",
}

# A list of preferred databases, in order. These databases will be
# displayed prominently in the "Add Database" dialog. You should
# use the "engine_name" attribute of the corresponding DB engine spec
# in `rabbitai/db_engine_specs/`.
PREFERRED_DATABASES: List[str] = [
    "PostgreSQL",
    "Presto",
    "MySQL",
    "SQLite",
    # etc.
]

# Do you want Talisman enabled?
TALISMAN_ENABLED = False
# If you want Talisman, how do you want it configured??
TALISMAN_CONFIG = {
    "content_security_policy": None,
    "force_https": True,
    "force_https_permanent": False,
}

# It is possible to customize which tables and roles are featured in the RLS
# dropdown. When set, this dict is assigned to `add_form_query_rel_fields` and
# `edit_form_query_rel_fields` on `RowLevelSecurityFiltersModelView`. Example:
#
# from flask_appbuilder.models.sqla import filters
# RLS_FORM_QUERY_REL_FIELDS = {
#     "roles": [["name", filters.FilterStartsWith, "RlsRole"]]
#     "tables": [["table_name", filters.FilterContains, "rls"]]
# }
RLS_FORM_QUERY_REL_FIELDS: Optional[Dict[str, List[List[Any]]]] = None
"""可以自定义行级安全RLS下拉列表中的表和角色。
设置后，此dict将分配给`RowLevelSecurityFiltersModelView`上的 `add_form_query_rel_fields` 和“编辑表单查询相关字段”。"""

# region Flask session cookie options
#
# See https://flask.palletsprojects.com/en/1.1.x/security/#set-cookie-options
# for details
#
SESSION_COOKIE_HTTPONLY = True  # Prevent cookie from being read by frontend JS?
SESSION_COOKIE_SECURE = False  # Prevent cookie from being transmitted over non-tls?
SESSION_COOKIE_SAMESITE = "Lax"  # One of [None, 'None', 'Lax', 'Strict']

# endregion

# Cache static resources.
SEND_FILE_MAX_AGE_DEFAULT = int(timedelta(days=365).total_seconds())
"""静态资源缓存时间（秒）。"""

# 存储示例数据的数据库地址 URI，如果设置为  `None`，则指向 SQLALCHEMY_DATABASE_URI
SQLALCHEMY_EXAMPLES_URI = None
"""存储示例数据的数据库地址 URI，如果设置为  `None`，则指向 SQLALCHEMY_DATABASE_URI"""

# Some sqlalchemy connection strings can open Rabbitai to security risks. Typically these should not be allowed.
PREVENT_UNSAFE_DB_CONNECTIONS = True
"""某些sqlalchemy连接字符串可能会使Rabbitai面临安全风险。通常，这些都是不允许的。"""

SSL_CERT_PATH: Optional[str] = None
"""用于存储使用自定义证书时生成的SSL证书的路径。默认为临时目录。例如：SSL_CERT_PATH = /certs"""

# region SIP-15

# SIP-15 should be enabled for all new Rabbitai deployments which ensures that the time
# range endpoints adhere to [start, end). For existing deployments admins should provide
# a dedicated period of time to allow chart producers to update their charts before
# mass migrating all charts to use the [start, end) interval.
#
# 注：如果未指定宽限期的结束日期，则宽限期是无限期的。
SIP_15_ENABLED = True
SIP_15_GRACE_PERIOD_END: Optional[date] = None  # exclusive
SIP_15_DEFAULT_TIME_RANGE_ENDPOINTS = ["unknown", "inclusive"]
SIP_15_TOAST_MESSAGE = (
    "Action Required: Preview then save your chart using the "
    'new time range endpoints <a target="_blank" href="{url}" '
    'class="alert-link">here</a>.'
)
# endregion

# Turn this key to False to disable ownership check on the old dataset MVC and
# datasource API /datasource/save.
#
# Warning: This config key is deprecated and will be removed in version 2.0.0"
OLD_API_CHECK_DATASET_OWNERSHIP = True

# SQLA table mutator, every time we fetch the metadata for a certain table
# (rabbitai.connectors.sqla.models.SqlaTable), we call this hook
# to allow mutating the object with this callback.
# This can be used to set any properties of the object based on naming
# conventions and such. You can find examples in the tests.
SQLA_TABLE_MUTATOR = lambda table: table
"""SQLA数据表转换器，每次我们获取某个表的元数据（rabbitai.connectors.sqla.models.SqlaTable）时，
我们调用这个钩子来允许使用这个回调来改变对象。这可用于根据命名约定等设置对象的任何属性。您可以在测试中找到示例。"""

# region 全局异步查询配置选项。

# 要求启用 GLOBAL_ASYNC_QUERIES 特性标志。
GLOBAL_ASYNC_QUERIES_REDIS_CONFIG = {
    "port": 6379,
    "host": "127.0.0.1",
    "password": "",
    "db": 0,
    "ssl": False,
}
GLOBAL_ASYNC_QUERIES_REDIS_STREAM_PREFIX = "async-events-"
GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT = 1000
GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT_FIREHOSE = 1000000
GLOBAL_ASYNC_QUERIES_JWT_COOKIE_NAME = "async-token"
GLOBAL_ASYNC_QUERIES_JWT_COOKIE_SECURE = False
GLOBAL_ASYNC_QUERIES_JWT_COOKIE_DOMAIN = None
GLOBAL_ASYNC_QUERIES_JWT_SECRET = "test-secret-change-me"
GLOBAL_ASYNC_QUERIES_TRANSPORT = "polling"
GLOBAL_ASYNC_QUERIES_POLLING_DELAY = int(
    timedelta(milliseconds=500).total_seconds() * 1000
)
GLOBAL_ASYNC_QUERIES_WEBSOCKET_URL = "ws://127.0.0.1:8080/"

# endregion

# SQL数据集运行状况检查。注：如果已启用，强烈建议将可调用项进行缓存以帮助提高性能，即：
#
#    @cache_manager.cache.memoize(timeout=0)
#    def DATASET_HEALTH_CHECK(datasource: SqlaTable) -> Optional[str]:
#        if (
#            datasource.sql and
#            len(sql_parse.ParsedQuery(datasource.sql, strip_comments=True).tables) == 1
#        ):
#            return (
#                "This virtual dataset queries only one table and therefore could be "
#                "replaced by querying the table directly."
#            )
#
#        return None
#
# Within the FLASK_APP_MUTATOR callable, i.e., once the application and thus cache have
# been initialized it is also necessary to add the following logic to blow the cache for
# all datasources if the callback function changed.
#
#    def FLASK_APP_MUTATOR(app: Flask) -> None:
#        name = "DATASET_HEALTH_CHECK"
#        func = app.config[name]
#        code = func.uncached.__code__.co_code
#
#        if cache_manager.cache.get(name) != code:
#            cache_manager.cache.delete_memoized(func)
#            cache_manager.cache.set(name, code, timeout=0)
#
DATASET_HEALTH_CHECK: Optional[Callable[["SqlaTable"], str]] = None
"""SQL数据集运行状况检查。注：如果已启用，强烈建议将可调用项进行缓存以帮助提高性能."""

# 不在菜单中显示用户信息或配置文件
MENU_HIDE_USER_INFO = False

# SQLalchemy 文档参考链接
SQLALCHEMY_DOCS_URL = "https://docs.sqlalchemy.org/en/13/core/engines.html"
SQLALCHEMY_DISPLAY_TEXT = "SQLAlchemy docs"

# -------------------------------------------------------------------
# *                警告:  不要编辑这里的内容                            *
# -------------------------------------------------------------------
# 不要在此行下方添加配置值，因为本地配置将无法覆盖它们。
if CONFIG_PATH_ENV_VAR in os.environ:
    # 显式导入不一定在pythonpath中的配置模块；适用于通过pex执行应用程序的情况。
    try:
        cfg_path = os.environ[CONFIG_PATH_ENV_VAR]
        module = sys.modules[__name__]
        override_conf = imp.load_source("rabbitai_config", cfg_path)
        for key in dir(override_conf):
            if key.isupper():
                setattr(module, key, getattr(override_conf, key))

        print(f"以从 [{cfg_path}] 加载本地配置")
    except Exception:
        logger.exception(
            "导入配置 %s=%s 失败", CONFIG_PATH_ENV_VAR, cfg_path
        )
        raise
elif importlib.util.find_spec("rabbitai_config") and not is_test():
    try:
        import rabbitai_config
        from . rabbitai_config import *

        print(f"已从 [{rabbitai_config.__file__}] 加载本地配置")
    except Exception:
        logger.exception("找到但加载本地 rabbitai_config 配置模块失败")
        raise
