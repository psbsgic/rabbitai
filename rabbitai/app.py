# -*- coding: utf-8 -*-

import logging
import os
from typing import Any, Callable, Dict

import wtforms_json
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

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    创建Flask实例，导入配置文件，并使用 APP_INITIALIZER 配置项指定的初始化器初始化各扩展模块。

    :return:
    """

    app = Flask(__name__)

    try:
        # 允许用户完全覆盖配置
        config_module = os.environ.get("RABBITAI_CONFIG", "rabbitai.config")
        app.config.from_object(config_module)

        app_initializer = app.config.get("APP_INITIALIZER", RabbitaiAppInitializer)(app)
        app_initializer.init_app()

        return app

    # 确保总是记录引导错误
    except Exception as ex:
        logger.exception("Failed to create app")
        raise ex


class RabbitaiIndexView(IndexView):
    """主页视图，定向到：/rabbitai/welcome/。"""

    @expose("/")
    def index(self) -> FlaskResponse:
        return redirect("/rabbitai/welcome/")


class RabbitaiAppInitializer:
    """应用扩展模块初始化器。"""

    def __init__(self, app: Flask) -> None:
        super().__init__()

        self.flask_app = app
        self.config = app.config
        self.manifest: Dict[Any, Any] = {}

    def init_app(self) -> None:
        """
        Main entry point which will delegate to other methods in
        order to fully init the app
        """

        self.pre_init()
        # Configuration of logging must be done first to apply the formatter properly
        self.configure_logging()
        self.configure_db_encrypt()
        self.setup_db()
        self.configure_celery()
        self.setup_event_logger()
        self.setup_bundle_manifest()
        self.register_blueprints()
        self.configure_wtf()
        self.configure_middlewares()
        self.configure_cache()

        with self.flask_app.app_context():
            self.init_app_in_ctx()

        self.post_init()

    def pre_init(self) -> None:
        """在所有其他init任务完成之前调用，初始化 wtforms_json，创建数据目录。"""

        wtforms_json.init()

        if not os.path.exists(self.config["DATA_DIR"]):
            os.makedirs(self.config["DATA_DIR"])

    def configure_logging(self) -> None:
        """配置日志。"""
        self.config["LOGGING_CONFIGURATOR"].configure_logging(
            self.config, self.flask_app.debug
        )

    def configure_db_encrypt(self) -> None:
        """配置数据库加密字段工厂。"""
        encrypted_field_factory.init_app(self.flask_app)

    def setup_db(self) -> None:
        """设置数据库。"""
        db.init_app(self.flask_app)

        with self.flask_app.app_context():
            pessimistic_connection_handling(db.engine)

        migrate.init_app(self.flask_app, db=db, directory=APP_DIR + "/migrations")

    def configure_celery(self) -> None:
        """配置 celery，确保对 celery 任务的每个调用都有一个正确的应用程序上下文设置。"""

        celery_app.config_from_object(self.config["CELERY_CONFIG"])
        celery_app.set_default()
        flask_app = self.flask_app

        # 在这里，我们要确保对芹菜任务的每个调用都有一个正确的应用程序上下文设置
        task_base = celery_app.Task

        class AppContextTask(task_base):
            """应用上下文任务，使 celery 任务的每个调用都有一个正确的应用程序上下文设置。"""
            abstract = True

            # 抓住任务中的每个调用并设置应用程序上下文
            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                with flask_app.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        celery_app.Task = AppContextTask

    def setup_event_logger(self) -> None:
        """设置事件日志。"""
        _event_logger["event_logger"] = get_event_logger_from_cfg_value(
            self.flask_app.config.get("EVENT_LOGGER", DBEventLogger())
        )

    def setup_bundle_manifest(self) -> None:
        """设置绑定资源清单"""
        manifest_processor.init_app(self.flask_app)

    def register_blueprints(self) -> None:
        """注册由配置对象提供的蓝图。"""

        for bp in self.config["BLUEPRINTS"]:
            try:
                logger.info("Registering blueprint: %s", bp.name)
                self.flask_app.register_blueprint(bp)
            except Exception:
                logger.exception("blueprint registration failed")

    def configure_wtf(self) -> None:
        """配置WTF。"""
        if self.config["WTF_CSRF_ENABLED"]:
            csrf.init_app(self.flask_app)
            csrf_exempt_list = self.config["WTF_CSRF_EXEMPT_LIST"]
            for ex in csrf_exempt_list:
                csrf.exempt(ex)

    def configure_middlewares(self) -> None:
        """配置中间件，CORS、wsgi_app、上传目录、压缩、talisman。"""

        if self.config["ENABLE_CORS"]:
            from flask_cors import CORS

            CORS(self.flask_app, **self.config["CORS_OPTIONS"])

        if self.config["ENABLE_PROXY_FIX"]:
            from werkzeug.middleware.proxy_fix import ProxyFix

            self.flask_app.wsgi_app = ProxyFix(
                self.flask_app.wsgi_app, **self.config["PROXY_FIX_CONFIG"]
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

            self.flask_app.wsgi_app = ChunkedEncodingFix(
                self.flask_app.wsgi_app
            )

        if self.config["UPLOAD_FOLDER"]:
            try:
                os.makedirs(self.config["UPLOAD_FOLDER"])
            except OSError:
                pass

        for middleware in self.config["ADDITIONAL_MIDDLEWARE"]:
            self.flask_app.wsgi_app = middleware(
                self.flask_app.wsgi_app
            )

        # Flask-Compress
        Compress(self.flask_app)

        if self.config["TALISMAN_ENABLED"]:
            talisman.init_app(self.flask_app, **self.config["TALISMAN_CONFIG"])

    def configure_cache(self) -> None:
        """配置缓存管理器"""
        cache_manager.init_app(self.flask_app)
        results_backend_manager.init_app(self.flask_app)

    # region in_ctx

    def init_app_in_ctx(self) -> None:
        """
        Runs init logic in the context of the app
        """

        self.configure_feature_flags()
        self.configure_fab()
        self.configure_url_map_converters()
        self.configure_data_sources()
        self.configure_auth_provider()
        self.configure_async_queries()

        # Hook that provides administrators a handle on the Flask APP after initialization
        flask_app_mutator = self.config["FLASK_APP_MUTATOR"]
        if flask_app_mutator:
            flask_app_mutator(self.flask_app)

        self.init_views()

    def configure_feature_flags(self) -> None:
        """配置功能标志管理器。"""
        feature_flag_manager.init_app(self.flask_app)

    def configure_fab(self) -> None:
        """配置 flask_appbuilder 对象实例，主要设置主页视图、安全管理器、基础Html模板。"""

        if self.config["SILENCE_FAB"]:
            logging.getLogger("flask_appbuilder").setLevel(logging.ERROR)

        custom_sm = self.config["CUSTOM_SECURITY_MANAGER"] or RabbitaiSecurityManager
        if not issubclass(custom_sm, RabbitaiSecurityManager):
            raise Exception(
                """Your CUSTOM_SECURITY_MANAGER must now extend RabbitaiSecurityManager,
                 not FAB's security manager.
                 See [4565] in UPDATING.md"""
            )

        appbuilder.indexview = RabbitaiIndexView
        appbuilder.base_template = "rabbitai/base.html"
        appbuilder.security_manager_class = custom_sm
        appbuilder.init_app(self.flask_app, db.session)

    def configure_url_map_converters(self) -> None:
        """配置 Flask 应用的 url_map.converters，添加 regex、object_type，使得通过正则表达式和对象类型查找到URL。"""
        #
        # Doing local imports here as model importing causes a reference to
        # app.config to be invoked and we need the current_app to have been setup
        #
        from rabbitai.utils.url_map_converters import (
            ObjectTypeConverter,
            RegexConverter,
        )

        self.flask_app.url_map.converters["regex"] = RegexConverter
        self.flask_app.url_map.converters["object_type"] = ObjectTypeConverter

    def configure_data_sources(self) -> None:
        """注册加载由配置对象提供的数据源。"""
        # Registering sources
        module_datasource_map = self.config["DEFAULT_MODULE_DS_MAP"]
        module_datasource_map.update(self.config["ADDITIONAL_MODULE_DS_MAP"])
        ConnectorRegistry.register_sources(module_datasource_map)

    def configure_auth_provider(self) -> None:
        """配置认证提供者。"""
        machine_auth_provider_factory.init_app(self.flask_app)

    def configure_async_queries(self) -> None:
        """配置异步查询。"""
        if feature_flag_manager.is_feature_enabled("GLOBAL_ASYNC_QUERIES"):
            async_query_manager.init_app(self.flask_app)

    def init_views(self) -> None:
        """
        初始化各API视图和常规视图。

        我们正在进行本地导入，因为其中一些导入了模型，而这些模型又试图导入全局Flask应用程序。

        :return:
        """

        # region 导入视图和API

        from rabbitai.annotation_layers.api import AnnotationLayerRestApi
        from rabbitai.annotation_layers.annotations.api import AnnotationRestApi
        from rabbitai.async_events.api import AsyncEventsRestApi
        from rabbitai.cachekeys.api import CacheRestApi
        from rabbitai.charts.api import ChartRestApi
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
        from rabbitai.views.api import Api
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
        from rabbitai.views.log.api import LogRestApi
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

        #  region Setup API views

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

        # region Setup regular views

        appbuilder.add_link(
            "Home",
            label=__("Home"),
            href="/rabbitai/welcome/",
            cond=lambda: bool(appbuilder.app.config["LOGO_TARGET_PATH"]),
        )
        appbuilder.add_view(
            AnnotationLayerModelView,
            "Annotation Layers",
            label=__("Annotation Layers"),
            icon="fa-comment",
            category="Manage",
            category_label=__("Manage"),
            category_icon="",
        )
        appbuilder.add_view(
            DatabaseView,
            "Databases",
            label=__("Databases"),
            icon="fa-database",
            category="Data",
            category_label=__("Data"),
            category_icon="fa-database",
        )
        appbuilder.add_link(
            "Datasets",
            label=__("Datasets"),
            href="/tablemodelview/list/",
            icon="fa-table",
            category="Data",
            category_label=__("Data"),
            category_icon="fa-table",
        )
        appbuilder.add_separator("Data")
        appbuilder.add_view(
            SliceModelView,
            "Charts",
            label=__("Charts"),
            icon="fa-bar-chart",
            category="",
            category_icon="",
        )
        appbuilder.add_view(
            DashboardModelView,
            "Dashboards",
            label=__("Dashboards"),
            icon="fa-dashboard",
            category="",
            category_icon="",
        )
        appbuilder.add_view(
            DynamicPluginsView,
            "Plugins",
            label=__("Plugins"),
            category="Manage",
            category_label=__("Manage"),
            icon="fa-puzzle-piece",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled(
                "DYNAMIC_PLUGINS"
            ),
        )
        appbuilder.add_view(
            CssTemplateModelView,
            "CSS Templates",
            label=__("CSS Templates"),
            icon="fa-css3",
            category="Manage",
            category_label=__("Manage"),
            category_icon="",
        )
        appbuilder.add_view(
            RowLevelSecurityFiltersModelView,
            "Row Level Security",
            label=__("Row level security"),
            category="Security",
            category_label=__("Security"),
            icon="fa-lock",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled(
                "ROW_LEVEL_SECURITY"
            ),
        )

        # endregion

        # region Setup views with no menu

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

        # region Add links

        appbuilder.add_link(
            "Import Dashboards",
            label=__("Import Dashboards"),
            href="/rabbitai/import_dashboards/",
            icon="fa-cloud-upload",
            category="Manage",
            category_label=__("Manage"),
            category_icon="fa-wrench",
            cond=lambda: not feature_flag_manager.is_feature_enabled(
                "VERSIONED_EXPORT"
            ),
        )
        appbuilder.add_link(
            "SQL Editor",
            label=_("SQL Editor"),
            href="/rabbitai/sqllab/",
            category_icon="fa-flask",
            icon="fa-flask",
            category="SQL Lab",
            category_label=__("SQL Lab"),
        )
        appbuilder.add_link(
            __("Saved Queries"),
            href="/savedqueryview/list/",
            icon="fa-save",
            category="SQL Lab",
        )
        appbuilder.add_link(
            "Query Search",
            label=_("Query History"),
            href="/rabbitai/sqllab/history/",
            icon="fa-search",
            category_icon="fa-flask",
            category="SQL Lab",
            category_label=__("SQL Lab"),
        )
        appbuilder.add_link(
            "Upload a CSV",
            label=__("Upload a CSV"),
            href="/csvtodatabaseview/form",
            icon="fa-upload",
            category="Data",
            category_label=__("Data"),
            category_icon="fa-wrench",
            cond=lambda: bool(
                self.config["CSV_EXTENSIONS"].intersection(
                    self.config["ALLOWED_EXTENSIONS"]
                )
            ),
        )

        try:
            import xlrd

            appbuilder.add_link(
                "Upload Excel",
                label=__("Upload Excel"),
                href="/exceltodatabaseview/form",
                icon="fa-upload",
                category="Data",
                category_label=__("Data"),
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
            label=__("Action Log"),
            category="Security",
            category_label=__("Security"),
            icon="fa-list-ol",
            menu_cond=lambda: (
                self.config["FAB_ADD_SECURITY_VIEWS"]
                and self.config["RABBITAI_LOG_VIEW"]
            ),
        )
        appbuilder.add_api(SecurityRestApi)

        # endregion

        # region Conditionally setup email views

        if self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"]:
            logging.warning(
                "ENABLE_SCHEDULED_EMAIL_REPORTS "
                "is deprecated and will be removed in version 2.0.0"
            )

        appbuilder.add_separator(
            "Manage", cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"]
        )
        appbuilder.add_view(
            DashboardEmailScheduleView,
            "Dashboard Email Schedules",
            label=__("Dashboard Emails"),
            category="Manage",
            category_label=__("Manage"),
            icon="fa-search",
            menu_cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"],
        )
        appbuilder.add_view(
            SliceEmailScheduleView,
            "Chart Emails",
            label=__("Chart Email Schedules"),
            category="Manage",
            category_label=__("Manage"),
            icon="fa-search",
            menu_cond=lambda: self.config["ENABLE_SCHEDULED_EMAIL_REPORTS"],
        )

        if self.config["ENABLE_ALERTS"]:
            logging.warning(
                "ENABLE_ALERTS is deprecated and will be removed in version 2.0.0"
            )

        appbuilder.add_view(
            AlertModelView,
            "Alerts",
            label=__("Alerts"),
            category="Manage",
            category_label=__("Manage"),
            icon="fa-exclamation-triangle",
            menu_cond=lambda: bool(self.config["ENABLE_ALERTS"]),
        )
        appbuilder.add_view_no_menu(AlertLogModelView)
        appbuilder.add_view_no_menu(AlertObservationModelView)

        appbuilder.add_view(
            AlertView,
            "Alerts & Report",
            label=__("Alerts & Reports"),
            category="Manage",
            category_label=__("Manage"),
            icon="fa-exclamation-triangle",
            menu_cond=lambda: feature_flag_manager.is_feature_enabled("ALERT_REPORTS"),
        )
        appbuilder.add_view_no_menu(ReportView)

        appbuilder.add_view(
            AccessRequestsModelView,
            "Access requests",
            label=__("Access requests"),
            category="Security",
            category_label=__("Security"),
            icon="fa-table",
            menu_cond=lambda: bool(self.config["ENABLE_ACCESS_REQUEST"]),
        )

        # endregion

        # region Druid Views

        """
        Druid是一个JDBC组件，它包括三部分： 

        1. DruidDriver 代理Driver，能够提供基于Filter－Chain模式的插件体系。 
        2. DruidDataSource 高效可管理的数据库连接池。 
        3. SQLParser 

        Druid可以做什么？ 

        1) 可以监控数据库访问性能，Druid内置提供了一个功能强大的StatFilter插件，能够详细统计SQL的执行性能，这对于线上分析数据库访问性能有帮助。 

        2) 替换DBCP和C3P0。Druid提供了一个高效、功能强大、可扩展性好的数据库连接池。 

        3) 数据库密码加密。直接把数据库密码写在配置文件中，这是不好的行为，容易导致安全问题。DruidDruiver和DruidDataSource都支持PasswordCallback。 

        4) SQL执行日志，Druid提供了不同的LogFilter，能够支持Common-Logging、Log4j和JdkLog，
        你可以按需要选择相应的LogFilter，监控你应用的数据库访问情况。 

        扩展JDBC，如果你要对JDBC层有编程的需求，可以通过Druid提供的Filter-Chain机制，很方便编写JDBC层的扩展插件。 
        """

        appbuilder.add_separator(
            "Data", cond=lambda: bool(self.config["DRUID_IS_ACTIVE"])
        )
        appbuilder.add_view(
            DruidDatasourceModelView,
            "Druid Datasources",
            label=__("Druid Datasources"),
            category="Data",
            category_label=__("Data"),
            icon="fa-cube",
            menu_cond=lambda: bool(self.config["DRUID_IS_ACTIVE"]),
        )
        appbuilder.add_view(
            DruidClusterModelView,
            name="Druid Clusters",
            label=__("Druid Clusters"),
            icon="fa-cubes",
            category="Data",
            category_label=__("Data"),
            category_icon="fa-database",
            menu_cond=lambda: bool(self.config["DRUID_IS_ACTIVE"]),
        )
        appbuilder.add_view_no_menu(DruidMetricInlineView)
        appbuilder.add_view_no_menu(DruidColumnInlineView)
        appbuilder.add_view_no_menu(Druid)

        appbuilder.add_link(
            "Scan New Datasources",
            label=__("Scan New Datasources"),
            href="/druid/scan_new_datasources/",
            category="Data",
            category_label=__("Data"),
            category_icon="fa-database",
            icon="fa-refresh",
            cond=lambda: bool(
                self.config["DRUID_IS_ACTIVE"]
                and self.config["DRUID_METADATA_LINKS_ENABLED"]
            ),
        )
        appbuilder.add_link(
            "Refresh Druid Metadata",
            label=__("Refresh Druid Metadata"),
            href="/druid/refresh_datasources/",
            category="Data",
            category_label=__("Data"),
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

    def post_init(self) -> None:
        """在任何其他初始化任务之后调用."""
