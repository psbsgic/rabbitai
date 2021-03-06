# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Dict, TYPE_CHECKING

import wtforms_json
from deprecation import deprecated
from flask import Flask, redirect
from flask_appbuilder import expose, IndexView
from flask_babel import gettext as __, lazy_gettext as _
from flask_compress import Compress

from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.extensions import (
    _event_logger,
    APP_DIR,
    appbuilder,
    async_query_manager,
    cache_manager,
    celery_app,
    csrf,
    db,
    encrypted_field_factory,
    feature_flag_manager,
    machine_auth_provider_factory,
    manifest_processor,
    migrate,
    results_backend_manager,
    talisman,
)
from rabbitai.security import RabbitaiSecurityManager
from rabbitai.typing import FlaskResponse
from rabbitai.utils.core import pessimistic_connection_handling
from rabbitai.utils.log import DBEventLogger, get_event_logger_from_cfg_value

if TYPE_CHECKING:
    from rabbitai.app import RabbitaiApp

logger = logging.getLogger(__name__)


class RabbitaiAppInitializer:
    """RabbitAI 应用初始化器，实施应用程序初始化工作，如配置，加载视图，构建菜单等。"""

    def __init__(self, app: RabbitaiApp) -> None:
        """
        使用指定要初始化的应用创建新实例。

        :param app: 要初始化的应用 RabbitaiApp。
        """

        super().__init__()

        self.rabbitai_app = app
        """Flask 应用实例"""
        self.config = app.config
        """应用的配置对象"""
        self.manifest: Dict[Any, Any] = {}
        """资源清单字典"""

    def init_app(self) -> None:
        """
        初始化应用程序的主入口点，调用其他方法以完全应用程序的初始化相关逻辑。

        - pre_init()：初始化应用前要调用的方法，初始化：wtforms_json，创建数据目录。
        - configure_logging()：配置日志系统。
        - configure_feature_flags()：配置特性标志，初始化特性标志管理器。
        - configure_db_encrypt()：配置数据库加密字段工厂。
        - setup_db()：配置数据库。
        - configure_celery()：配置 celery_app，以便执行并行分布式异步任务。
        - setup_event_logger()：依据应用配置 EVENT_LOGGER 提供的值获取事件日志记录器，并缓存在：_event_logger 中。
        - setup_bundle_manifest()：配置中间件。
        - register_blueprints()：注册配置提供的蓝图。
        - configure_wtf()：配置 WTF。
        - configure_middlewares()：配置中间件。
        - configure_cache()：配置缓存，缓存管理器和结果后端管理器。
        - init_app_in_ctx()：在应用上下文中执行初始化逻辑。
        - post_init()：初始化工作完成后要调用的方法。

        """

        self.pre_init()
        # 必须先配置日志，才能正确应用格式化程序
        self.configure_logging()
        # 必须首先配置feature_flags，以便有条件地允许init功能
        self.configure_feature_flags()
        self.configure_db_encrypt()
        self.setup_db()
        self.configure_celery()
        self.setup_event_logger()
        self.setup_bundle_manifest()
        self.register_blueprints()
        self.configure_wtf()
        self.configure_middlewares()
        self.configure_cache()

        with self.rabbitai_app.app_context():
            self.init_app_in_ctx()

        self.post_init()

    def pre_init(self) -> None:
        """初始化应用前要调用的方法，初始化：wtforms_json，创建数据目录。"""

        wtforms_json.init()

        if not os.path.exists(self.config["DATA_DIR"]):
            os.makedirs(self.config["DATA_DIR"])

    def post_init(self) -> None:
        """初始化工作完成后要调用的方法。"""

    def configure_celery(self) -> None:
        """
        配置 celery_app，以便执行并行分布式异步任务。

        celery用在需要耗时的操作中，主进程把任务放在任务队列中，celery从任务队列中取出并执行，
        执行完毕结果放入backend中，主进程去backend里取。
        """

        celery_app.config_from_object(self.config["CELERY_CONFIG"])
        celery_app.set_default()
        rabbitai_app = self.rabbitai_app

        # 在这里，我们希望确保对 celery 任务的每个调用都有一个正确的应用程序上下文设置
        task_base = celery_app.Task

        class AppContextTask(task_base):
            """基于应用上下文的任务，在应用的上下文 app_context 中调用该任务。"""
            abstract = True

            # 抓取任务中的每个调用并设置应用程序上下文
            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                with rabbitai_app.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        celery_app.Task = AppContextTask

    # region init_app_in_ctx

    def init_app_in_ctx(self) -> None:
        """在应用上下文中执行初始化逻辑。

        - 配置Flask应用构建者，设置日志级别、安全管理器、主页视图、基础模板、安全管理器，并初始化Flask应用构建者。
        - 配置Url映射转换器，添加：RegexConverter、ObjectTypeConverter。
        - 配置数据源，从配置对象中加载 DEFAULT_MODULE_DS_MAP、ADDITIONAL_MODULE_DS_MAP 并注册到连接器注册表。
        - 配置认证提供者。
        - 配置并初始化异步查询管理器 `async_query_manager`。
        - 初始化所有视图，导入所有视图，设置API视图、常规视图。
        """

        self.configure_fab()
        self.configure_url_map_converters()
        self.configure_data_sources()
        self.configure_auth_provider()
        self.configure_async_queries()

        # 在初始化后为管理员提供Flask应用程序句柄的钩子
        flask_app_mutator = self.config["FLASK_APP_MUTATOR"]
        if flask_app_mutator:
            flask_app_mutator(self.rabbitai_app)

        self.init_views()

    def configure_fab(self) -> None:
        """配置Flask应用构建者，设置日志级别、安全管理器、主页视图、基础模板、安全管理器，并初始化Flask应用构建者。"""

        # 构建并配置 flask_appbuilder 日志
        if self.config["SILENCE_FAB"]:
            logging.getLogger("flask_appbuilder").setLevel(logging.ERROR)

        # 自定义安全管理器
        custom_sm = self.config["CUSTOM_SECURITY_MANAGER"] or RabbitaiSecurityManager
        if not issubclass(custom_sm, RabbitaiSecurityManager):
            raise Exception(
                """Your CUSTOM_SECURITY_MANAGER must now extend RabbitaiSecurityManager,
                 not FAB's security manager.
                 See [4565] in UPDATING.md"""
            )

        # 配置应用构建者
        appbuilder.indexview = RabbitaiIndexView
        appbuilder.base_template = "rabbitai/base.html"
        appbuilder.security_manager_class = custom_sm
        appbuilder.init_app(self.rabbitai_app, db.session)

    def configure_url_map_converters(self) -> None:
        """配置Url映射转换器，添加：RegexConverter、ObjectTypeConverter。"""

        #
        # Doing local imports here as model importing causes a reference to
        # app.config to be invoked and we need the current_app to have been setup
        #
        from rabbitai.utils.url_map_converters import (
            ObjectTypeConverter,
            RegexConverter,
        )

        self.rabbitai_app.url_map.converters["regex"] = RegexConverter
        self.rabbitai_app.url_map.converters["object_type"] = ObjectTypeConverter

    def configure_data_sources(self) -> None:
        """配置数据源，从配置对象中加载 DEFAULT_MODULE_DS_MAP、ADDITIONAL_MODULE_DS_MAP 并注册到连接器注册表。"""

        # 注册数据源，模块名称及其定义的数据源类型列表的字典
        module_datasource_map = self.config["DEFAULT_MODULE_DS_MAP"]
        module_datasource_map.update(self.config["ADDITIONAL_MODULE_DS_MAP"])
        ConnectorRegistry.register_sources(module_datasource_map)

    def configure_auth_provider(self) -> None:
        """配置认证提供者。"""

        machine_auth_provider_factory.init_app(self.rabbitai_app)

    def configure_async_queries(self) -> None:
        """配置并初始化异步查询管理器 `async_query_manager`。"""
        if feature_flag_manager.is_feature_enabled("GLOBAL_ASYNC_QUERIES"):
            async_query_manager.init_app(self.rabbitai_app)

    def init_views(self) -> None:
        """初始化所有视图，导入所有视图，设置API视图、常规视图。"""

        # region 导入视图

        # region api
        from rabbitai.annotation_layers.api import AnnotationLayerRestApi
        from rabbitai.annotation_layers.annotations.api import AnnotationRestApi
        from rabbitai.async_events.api import AsyncEventsRestApi
        from rabbitai.cachekeys.api import CacheRestApi
        from rabbitai.charts.api import ChartRestApi
        from rabbitai.css_templates.api import CssTemplateRestApi
        from rabbitai.dashboards.api import DashboardRestApi
        from rabbitai.databases.api import DatabaseRestApi
        from rabbitai.datasets.api import DatasetRestApi
        from rabbitai.datasets.columns.api import DatasetColumnsRestApi
        from rabbitai.datasets.metrics.api import DatasetMetricRestApi
        from rabbitai.queries.api import QueryRestApi
        from rabbitai.security.api import SecurityRestApi
        from rabbitai.queries.saved_queries.api import SavedQueryRestApi
        from rabbitai.reports.api import ReportScheduleRestApi
        from rabbitai.reports.logs.api import ReportExecutionLogRestApi
        from rabbitai.views.api import Api
        from rabbitai.views.log.api import LogRestApi
        # endregion

        # region rabbitai.connectors

        from rabbitai.connectors.druid.views import (
            Druid,
            DruidClusterModelView,
            DruidColumnInlineView,
            DruidDatasourceModelView,
            DruidMetricInlineView,
        )
        from rabbitai.connectors.sqla.views import (
            RowLevelSecurityFiltersModelView,
            SqlMetricInlineView,
            TableColumnInlineView,
            TableModelView,
        )
        # endregion

        # region rabbitai.views
        from rabbitai.views.access_requests import AccessRequestsModelView
        from rabbitai.views.alerts import (
            AlertLogModelView,
            AlertModelView,
            AlertObservationModelView,
            AlertView,
            ReportView,
        )
        from rabbitai.views.annotations import (
            AnnotationLayerModelView,
            AnnotationModelView,
        )

        from rabbitai.views.chart.views import SliceAsync, SliceModelView
        from rabbitai.views.core import Rabbitai
        from rabbitai.views.css_templates import (
            CssTemplateAsyncModelView,
            CssTemplateModelView,
        )
        from rabbitai.views.dashboard.views import (
            Dashboard,
            DashboardModelView,
            DashboardModelViewAsync,
        )
        from rabbitai.views.database.views import (
            CsvToDatabaseView,
            DatabaseView,
            ExcelToDatabaseView,
        )
        from rabbitai.views.datasource import Datasource
        from rabbitai.views.dynamic_plugins import DynamicPluginsView
        from rabbitai.views.key_value import KV

        from rabbitai.views.log.views import LogModelView
        from rabbitai.views.redirects import R
        from rabbitai.views.schedules import (
            DashboardEmailScheduleView,
            SliceEmailScheduleView,
        )
        from rabbitai.views.sql_lab import (
            SavedQueryView,
            SavedQueryViewApi,
            SqlLab,
            TableSchemaView,
            TabStateView,
        )
        from rabbitai.views.tags import TagView
        # endregion

        # endregion

        #  region 设置 API 视图

        appbuilder.add_api(AnnotationRestApi)
        appbuilder.add_api(AnnotationLayerRestApi)
        appbuilder.add_api(AsyncEventsRestApi)
        appbuilder.add_api(CacheRestApi)
        appbuilder.add_api(ChartRestApi)
        appbuilder.add_api(CssTemplateRestApi)
        appbuilder.add_api(DashboardRestApi)
        appbuilder.add_api(DatabaseRestApi)
        appbuilder.add_api(DatasetRestApi)
        appbuilder.add_api(DatasetColumnsRestApi)
        appbuilder.add_api(DatasetMetricRestApi)
        appbuilder.add_api(QueryRestApi)
        appbuilder.add_api(SavedQueryRestApi)
        appbuilder.add_api(ReportScheduleRestApi)
        appbuilder.add_api(ReportExecutionLogRestApi)

        # endregion

        # region 设置常规视图

        appbuilder.add_link(
            "Home",
            label="主页",
            href="/rabbitai/welcome/",
            cond=lambda: bool(appbuilder.app.config["LOGO_TARGET_PATH"]),
        )
        appbuilder.add_view(
            AnnotationLayerModelView,
            "Annotation Layers",
            label="注释层",
            icon="fa-comment",
            category="Manage",
            category_label="管理",
            category_icon="",
        )
        appbuilder.add_view(
            DashboardModelView,
            "Dashboards",
            label="仪表盘",
            icon="fa-dashboard",
            category="",
            category_icon="",
        )
        appbuilder.add_view(
            SliceModelView,
            "Charts",
            label="图表",
            icon="fa-bar-chart",
            category="",
            category_icon="",
        )
        appbuilder.add_view(
            DynamicPluginsView,
            "Plugins",
            label="插件",
            category="Manage",
            category_label="管理",
            icon="fa-puzzle-piece",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled(
                "DYNAMIC_PLUGINS"
            ),
        )
        appbuilder.add_view(
            CssTemplateModelView,
            "CSS Templates",
            label="CSS 模板",
            icon="fa-css3",
            category="Manage",
            category_label="管理",
            category_icon="",
        )
        appbuilder.add_view(
            RowLevelSecurityFiltersModelView,
            "Row Level Security",
            label="行级安全",
            category="Security",
            category_label="安全",
            icon="fa-lock",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled(
                "ROW_LEVEL_SECURITY"
            ),
        )

        # endregion

        # region 设置没有菜单的视图

        appbuilder.add_view_no_menu(Api)
        appbuilder.add_view_no_menu(CssTemplateAsyncModelView)
        appbuilder.add_view_no_menu(CsvToDatabaseView)
        appbuilder.add_view_no_menu(ExcelToDatabaseView)
        appbuilder.add_view_no_menu(Dashboard)
        appbuilder.add_view_no_menu(DashboardModelViewAsync)
        appbuilder.add_view_no_menu(Datasource)
        appbuilder.add_view_no_menu(KV)
        appbuilder.add_view_no_menu(R)
        appbuilder.add_view_no_menu(SavedQueryView)
        appbuilder.add_view_no_menu(SavedQueryViewApi)
        appbuilder.add_view_no_menu(SliceAsync)
        appbuilder.add_view_no_menu(SqlLab)
        appbuilder.add_view_no_menu(SqlMetricInlineView)
        appbuilder.add_view_no_menu(AnnotationModelView)
        appbuilder.add_view_no_menu(Rabbitai)
        appbuilder.add_view_no_menu(TableColumnInlineView)
        appbuilder.add_view_no_menu(TableModelView)
        appbuilder.add_view_no_menu(TableSchemaView)
        appbuilder.add_view_no_menu(TabStateView)
        appbuilder.add_view_no_menu(TagView)

        # endregion

        # region 添加链接

        appbuilder.add_link(
            "Import Dashboards",
            label="导入仪表盘",
            href="/rabbitai/import_dashboards/",
            icon="fa-cloud-upload",
            category="Manage",
            category_label="管理",
            category_icon="fa-wrench",
            cond=lambda: not feature_flag_manager.is_feature_enabled(
                "VERSIONED_EXPORT"
            ),
        )
        appbuilder.add_link(
            "SQL Editor",
            label="SQL 编辑器",
            href="/rabbitai/sqllab/",
            category_icon="fa-flask",
            icon="fa-flask",
            category="SQL Lab",
            category_label="SQL 工具箱",
        )
        appbuilder.add_link(
            "Saved Query",
            label="保存的查询",
            href="/savedqueryview/list/",
            icon="fa-save",
            category="SQL Lab",
            category_label="SQL 工具箱",
        )
        appbuilder.add_link(
            "Query Search",
            label="查询记录",  # Query History,
            href="/rabbitai/sqllab/history/",
            icon="fa-search",
            category_icon="fa-flask",
            category="SQL Lab",
            category_label="SQL 工具箱",
        )
        appbuilder.add_view(
            DatabaseView,
            "Databases",
            label="数据库",
            icon="fa-database",
            category="Data",
            category_label="数据",
            category_icon="fa-database",
        )
        appbuilder.add_link(
            "Datasets",
            label="数据集",
            href="/tablemodelview/list/",
            icon="fa-table",
            category="Data",
            category_label="数据",
            category_icon="fa-table",
        )
        appbuilder.add_separator("Data")
        appbuilder.add_link(
            "Upload a CSV",
            label="上传 CSV 文件",
            href="/csvtodatabaseview/form",
            icon="fa-upload",
            category="Data",
            category_label="数据",
            category_icon="fa-wrench",
            cond=lambda: bool(
                self.config["CSV_EXTENSIONS"].intersection(
                    self.config["ALLOWED_EXTENSIONS"]
                )
            ),
        )

        try:
            import xlrd  # pylint: disable=unused-import

            appbuilder.add_link(
                "Upload Excel",
                label="上传 Excel 文件",
                href="/exceltodatabaseview/form",
                icon="fa-upload",
                category="Data",
                category_label="数据",
                category_icon="fa-wrench",
                cond=lambda: bool(
                    self.config["EXCEL_EXTENSIONS"].intersection(
                        self.config["ALLOWED_EXTENSIONS"]
                    )
                ),
            )
        except ImportError:
            pass

        appbuilder.add_api(LogRestApi)
        appbuilder.add_view(
            LogModelView,
            "Action Log",
            label="操作日志",
            category="Security",
            category_label="安全",
            icon="fa-list-ol",
            menu_cond=lambda: (
                self.config["FAB_ADD_SECURITY_VIEWS"]
                and self.config["RABBITAI_LOG_VIEW"]
            ),
        )
        appbuilder.add_api(SecurityRestApi)

        # endregion

        # region 设置 email 视图

        appbuilder.add_separator(
            "Manage", cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"]
        )
        appbuilder.add_view(
            DashboardEmailScheduleView,
            "Dashboard Email Schedules",
            label="仪表盘邮件",  # Dashboard Emails
            category="Manage",
            category_label="管理",
            icon="fa-search",
            menu_cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"],
        )
        appbuilder.add_view(
            SliceEmailScheduleView,
            "Chart Emails",
            label="图表邮件计划",  # Chart Email Schedules
            category="Manage",
            category_label="管理",
            icon="fa-search",
            menu_cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"],
        )

        appbuilder.add_view(
            AlertModelView,
            "Alerts",
            label="提醒警告",
            category="Manage",
            category_label="管理",
            icon="fa-exclamation-triangle",
            menu_cond=lambda: bool(self.config["ENABLE_ALERTS"]),
        )
        appbuilder.add_view_no_menu(AlertLogModelView)
        appbuilder.add_view_no_menu(AlertObservationModelView)

        appbuilder.add_view(
            AlertView,
            "Alerts & Report",
            label="提醒 & 报告",
            category="Manage",
            category_label="管理",
            icon="fa-exclamation-triangle",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled("ALERT_REPORTS"),
        )
        appbuilder.add_view_no_menu(ReportView)

        appbuilder.add_view(
            AccessRequestsModelView,
            "Access requests",
            label="访问请求",
            category="Security",
            category_label="安全",
            icon="fa-table",
            menu_cond=lambda: bool(self.config["ENABLE_ACCESS_REQUEST"]),
        )

        # endregion

        # region Druid 视图

        appbuilder.add_separator(
            "Data", cond=lambda: bool(self.config["DRUID_IS_ACTIVE"])
        )
        appbuilder.add_view(
            DruidDatasourceModelView,
            "Druid Datasources",
            label="Druid 数据源",
            category="Data",
            category_label="数据",
            icon="fa-cube",
            menu_cond=lambda: bool(self.config["DRUID_IS_ACTIVE"]),
        )
        appbuilder.add_view(
            DruidClusterModelView,
            name="Druid Clusters",
            label="Druid 集群",
            icon="fa-cubes",
            category="Data",
            category_label="数据",
            category_icon="fa-database",
            menu_cond=lambda: bool(self.config["DRUID_IS_ACTIVE"]),
        )
        appbuilder.add_view_no_menu(DruidMetricInlineView)
        appbuilder.add_view_no_menu(DruidColumnInlineView)
        appbuilder.add_view_no_menu(Druid)

        appbuilder.add_link(
            "Scan New Datasources",
            label="扫描新数据源",
            href="/druid/scan_new_datasources/",
            category="Data",
            category_label="数据",
            category_icon="fa-database",
            icon="fa-refresh",
            cond=lambda: bool(
                self.config["DRUID_IS_ACTIVE"]
                and self.config["DRUID_METADATA_LINKS_ENABLED"]
            ),
        )
        appbuilder.add_link(
            "Refresh Druid Metadata",
            label="刷新 Druid 元数据",
            href="/druid/refresh_datasources/",
            category="Data",
            category_label="数据",
            category_icon="fa-database",
            icon="fa-cog",
            cond=lambda: bool(
                self.config["DRUID_IS_ACTIVE"]
                and self.config["DRUID_METADATA_LINKS_ENABLED"]
            ),
        )
        appbuilder.add_separator(
            "Data", cond=lambda: bool(self.config["DRUID_IS_ACTIVE"])
        )

        # endregion

    # endregion

    def setup_event_logger(self) -> None:
        """依据应用配置 EVENT_LOGGER 提供的值获取事件日志记录器，并缓存在：_event_logger 中。"""
        _event_logger["event_logger"] = get_event_logger_from_cfg_value(
            self.rabbitai_app.config.get("EVENT_LOGGER", DBEventLogger())
        )

    def configure_cache(self) -> None:
        """配置缓存，缓存管理器和结果后端管理器。"""
        cache_manager.init_app(self.rabbitai_app)
        results_backend_manager.init_app(self.rabbitai_app)

    def configure_feature_flags(self) -> None:
        """配置特性标志，初始化特性标志管理器。"""
        feature_flag_manager.init_app(self.rabbitai_app)

    def configure_middlewares(self) -> None:
        """配置中间件，配置 CORS。"""

        if self.config["ENABLE_CORS"]:
            from flask_cors import CORS

            CORS(self.rabbitai_app, **self.config["CORS_OPTIONS"])

        if self.config["ENABLE_PROXY_FIX"]:
            from werkzeug.middleware.proxy_fix import ProxyFix

            self.rabbitai_app.wsgi_app = ProxyFix(  # type: ignore
                self.rabbitai_app.wsgi_app, **self.config["PROXY_FIX_CONFIG"]
            )

        if self.config["ENABLE_CHUNK_ENCODING"]:

            class ChunkedEncodingFix:
                def __init__(self, app: Flask) -> None:
                    self.app = app

                def __call__(
                    self, environ: Dict[str, Any], start_response: Callable[..., Any]
                ) -> Any:
                    # Setting wsgi.input_terminated tells werkzeug.wsgi to ignore
                    # content-length and read the stream till the end.
                    if environ.get("HTTP_TRANSFER_ENCODING", "").lower() == "chunked":
                        environ["wsgi.input_terminated"] = True
                    return self.app(environ, start_response)

            self.rabbitai_app.wsgi_app = ChunkedEncodingFix(
                self.rabbitai_app.wsgi_app
            )

        if self.config["UPLOAD_FOLDER"]:
            try:
                os.makedirs(self.config["UPLOAD_FOLDER"])
            except OSError:
                pass

        for middleware in self.config["ADDITIONAL_MIDDLEWARE"]:
            self.rabbitai_app.wsgi_app = middleware(self.rabbitai_app.wsgi_app)

        # Flask-Compress
        Compress(self.rabbitai_app)

        if self.config["TALISMAN_ENABLED"]:
            talisman.init_app(self.rabbitai_app, **self.config["TALISMAN_CONFIG"])

    def configure_logging(self) -> None:
        """配置日志系统。"""
        self.config["LOGGING_CONFIGURATOR"].configure_logging(
            self.config, self.rabbitai_app.debug
        )

    def configure_db_encrypt(self) -> None:
        """配置数据库加密，读取加密相关配置。"""
        encrypted_field_factory.init_app(self.rabbitai_app)

    def setup_db(self) -> None:
        """设置数据库，监听数据库连接并测试有效性。"""

        db.init_app(self.rabbitai_app)

        with self.rabbitai_app.app_context():
            pessimistic_connection_handling(db.engine)

        migrate.init_app(self.rabbitai_app, db=db, directory=APP_DIR + "/migrations")

    def configure_wtf(self) -> None:
        """配置 wtf，标记配置对象 WTF_CSRF_EXEMPT_LIST 的视图或蓝图为排除 CSRF 保护。"""

        if self.config["WTF_CSRF_ENABLED"]:
            csrf.init_app(self.rabbitai_app)
            csrf_exempt_list = self.config["WTF_CSRF_EXEMPT_LIST"]
            for ex in csrf_exempt_list:
                csrf.exempt(ex)

    def register_blueprints(self) -> None:
        """注册应用配置 BLUEPRINTS 选项提供的蓝图。"""

        for bp in self.config["BLUEPRINTS"]:
            try:
                logger.info("Registering blueprint: %s", bp.name)
                self.rabbitai_app.register_blueprint(bp)
            except Exception:
                logger.exception("blueprint registration failed")

    def setup_bundle_manifest(self) -> None:
        """设置并初始化打包资源清单处理器。"""

        manifest_processor.init_app(self.rabbitai_app)


class RabbitaiIndexView(IndexView):
    """Rabbitai主页视图，将主页重定向到 /rabbitai/welcome/。"""

    @expose("/")
    def index(self) -> FlaskResponse:
        return redirect("/rabbitai/welcome/")
