# -*- coding: utf-8 -*-

import dataclasses  # pylint: disable=wrong-import-order
import functools
import logging
import traceback
from datetime import datetime
from typing import Any, Callable, cast, Dict, List, Optional, TYPE_CHECKING, Union

import simplejson as json
import yaml
from flask import (
    abort,
    flash,
    g,
    get_flashed_messages,
    redirect,
    request,
    Response,
    send_file,
    session,
)
from flask_appbuilder import BaseView, Model, ModelView
from flask_appbuilder.actions import action
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.models.sqla.filters import BaseFilter
from flask_appbuilder.security.sqla.models import Role, User
from flask_appbuilder.widgets import ListWidget
from flask_babel import get_locale, gettext as __, lazy_gettext as _
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_wtf.csrf import CSRFError
from flask_wtf.form import FlaskForm
from pkg_resources import resource_filename
from sqlalchemy import or_
from sqlalchemy.orm import Query
from werkzeug.exceptions import HTTPException
from wtforms import Form
from wtforms.fields.core import Field, UnboundField

from rabbitai import (
    app as rabbitai_app,
    appbuilder,
    conf,
    db,
    get_feature_flags,
    security_manager,
)
from rabbitai.commands.exceptions import CommandException, CommandInvalidError
from rabbitai.connectors.sqla import models
from rabbitai.datasets.commands.exceptions import get_dataset_exist_error_msg
from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import (
    RabbitaiErrorException,
    RabbitaiErrorsException,
    RabbitaiException,
    RabbitaiSecurityException,
)
from rabbitai.models.helpers import ImportExportMixin
from rabbitai.translations.utils import get_language_pack
from rabbitai.typing import FlaskResponse
from rabbitai.utils import core as utils

from .utils import bootstrap_user_data

if TYPE_CHECKING:
    from rabbitai.connectors.druid.views import (
        DruidClusterModelView,
    )

FRONTEND_CONF_KEYS = (
    "RABBITAI_WEBSERVER_TIMEOUT",
    "RABBITAI_DASHBOARD_POSITION_DATA_LIMIT",
    "RABBITAI_DASHBOARD_PERIODICAL_REFRESH_LIMIT",
    "RABBITAI_DASHBOARD_PERIODICAL_REFRESH_WARNING_MESSAGE",
    "DISABLE_DATASET_SOURCE_EDIT",
    "DRUID_IS_ACTIVE",
    "ENABLE_JAVASCRIPT_CONTROLS",
    "DEFAULT_SQLLAB_LIMIT",
    "DEFAULT_VIZ_TYPE",
    "SQL_MAX_ROW",
    "RABBITAI_WEBSERVER_DOMAINS",
    "SQLLAB_SAVE_WARNING_MESSAGE",
    "DISPLAY_MAX_ROW",
    "GLOBAL_ASYNC_QUERIES_TRANSPORT",
    "GLOBAL_ASYNC_QUERIES_POLLING_DELAY",
    "SQLALCHEMY_DOCS_URL",
    "SQLALCHEMY_DISPLAY_TEXT",
    "GLOBAL_ASYNC_QUERIES_WEBSOCKET_URL",
)
"""前端配置键列表，这些键提供要传递到前端的数据，可以通过后端（Flask）的配置对象相应键来进行设置。"""

logger = logging.getLogger(__name__)

config = rabbitai_app.config


def get_error_msg() -> str:
    """获取错误信息。"""

    if conf.get("SHOW_STACKTRACE"):
        error_msg = traceback.format_exc()
    else:
        error_msg = "FATAL ERROR \n"
        error_msg += (
            "Stacktrace is hidden. Change the SHOW_STACKTRACE "
            "configuration setting to enable it"
        )
    return error_msg


def json_error_response(
    msg: Optional[str] = None,
    status: int = 500,
    payload: Optional[Dict[str, Any]] = None,
    link: Optional[str] = None,
) -> FlaskResponse:
    """
    返回单个错误信息响应对象。

    :param msg: 错误信息。
    :param status: 状态码。
    :param payload: 响应的字典内容。
    :param link: 链接地址。
    :return: FlaskResponse 实例。
    """

    if not payload:
        payload = {"error": "{}".format(msg)}
    if link:
        payload["link"] = link

    return Response(
        json.dumps(payload, default=utils.json_iso_dttm_ser, ignore_nan=True),
        status=status,
        mimetype="application/json",
    )


def json_errors_response(
    errors: List[RabbitaiError],
    status: int = 500,
    payload: Optional[Dict[str, Any]] = None,
) -> FlaskResponse:
    """
    返回错误响应对象。

    :param errors: 错误对象列表。
    :param status: 状态。
    :param payload: 响应的字典内容。
    :return: FlaskResponse 实例。
    """

    if not payload:
        payload = {}

    payload["errors"] = [dataclasses.asdict(error) for error in errors]
    return Response(
        json.dumps(payload, default=utils.json_iso_dttm_ser, ignore_nan=True),
        status=status,
        mimetype="application/json; charset=utf-8",
    )


def json_success(json_msg: str, status: int = 200) -> FlaskResponse:
    """
    返回成功的响应对象。

    :param json_msg:
    :param status:
    :return:
    """

    return Response(json_msg, status=status, mimetype="application/json")


def data_payload_response(payload_json: str, has_error: bool = False) -> FlaskResponse:
    """
    获取数据载荷响应对象。

    :param payload_json: 载荷Json对象。
    :param has_error:
    :return:
    """

    status = 400 if has_error else 200
    return json_success(payload_json, status=status)


def generate_download_headers(extension: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    生成下载标头字典。

    :param extension: 文件扩展名称。
    :param filename: 文件名称。
    :return:
    """

    filename = filename if filename else datetime.now().strftime("%Y%m%d_%H%M%S")
    content_disp = f"attachment; filename={filename}.{extension}"
    headers = {"Content-Disposition": content_disp}
    return headers


def api(f: Callable[..., FlaskResponse]) -> Callable[..., FlaskResponse]:
    """
    一个装饰器，标记一个端点为 API，捕获未捕获的异常并以JSON格式返回响应。

    :param f: 被装饰的函数。
    :type f:
    :return:
    :rtype:
    """

    def wraps(self: "BaseRabbitaiView", *args: Any, **kwargs: Any) -> FlaskResponse:
        try:
            return f(self, *args, **kwargs)
        except NoAuthorizationError as ex:  # pylint: disable=broad-except
            logger.warning(ex)
            return json_error_response(get_error_msg(), status=401)
        except Exception as ex:  # pylint: disable=broad-except
            logger.exception(ex)
            return json_error_response(get_error_msg())

    return functools.update_wrapper(wraps, f)


def handle_api_exception(f: Callable[..., FlaskResponse]) -> Callable[..., FlaskResponse]:
    """
    一个捕获并处理 rabbitai 异常的装饰器。在 @api 装饰器后使用它以便在一般异常处理前处理 rabbitai 异常。
    """

    def wraps(self: "BaseRabbitaiView", *args: Any, **kwargs: Any) -> FlaskResponse:
        try:
            return f(self, *args, **kwargs)
        except RabbitaiSecurityException as ex:
            logger.warning(ex)
            return json_errors_response(
                errors=[ex.error], status=ex.status, payload=ex.payload
            )
        except RabbitaiErrorsException as ex:
            logger.warning(ex, exc_info=True)
            return json_errors_response(errors=ex.errors, status=ex.status)
        except RabbitaiErrorException as ex:
            logger.warning(ex)
            return json_errors_response(errors=[ex.error], status=ex.status)
        except RabbitaiException as ex:
            if ex.status >= 500:
                logger.exception(ex)
            return json_error_response(
                utils.error_msg_from_exception(ex), status=ex.status
            )
        except HTTPException as ex:
            logger.exception(ex)
            return json_error_response(
                utils.error_msg_from_exception(ex), status=cast(int, ex.code)
            )
        except Exception as ex:  # pylint: disable=broad-except
            logger.exception(ex)
            return json_error_response(utils.error_msg_from_exception(ex))

    return functools.update_wrapper(wraps, f)


def validate_sqlatable(table: models.SqlaTable) -> None:
    """
    检查指定SQL数据表对象是否存在，不存在则引发异常。

    :param table: SQL数据表对象。
    :return:
    """

    with db.session.no_autoflush:
        table_query = db.session.query(models.SqlaTable).filter(
            models.SqlaTable.table_name == table.table_name,
            models.SqlaTable.schema == table.schema,
            models.SqlaTable.database_id == table.database.id,
        )
        if db.session.query(table_query.exists()).scalar():
            raise Exception(get_dataset_exist_error_msg(table.full_name))

    # Fail before adding if the table can't be found
    try:
        table.get_sqla_table_object()
    except Exception as ex:
        logger.exception("Got an error in pre_add for %s", table.name)
        raise Exception(
            _(
                "Table [%{table}s] could not be found, "
                "please double check your "
                "database connection, schema, and "
                "table name, error: {}"
            ).format(table.name, str(ex))
        )


def create_table_permissions(table: models.SqlaTable) -> None:
    """
    获取指定数据表的权限并作为权限视图菜单添加到安全管理器。

    :param table: 数据表。
    :return:
    """

    security_manager.add_permission_view_menu("datasource_access", table.get_perm())
    if table.schema:
        security_manager.add_permission_view_menu("schema_access", table.schema_perm)


def get_user_roles() -> List[Role]:
    """获取当前用户的所有角色对象。"""

    if g.user.is_anonymous:
        public_role = conf.get("AUTH_ROLE_PUBLIC")
        return [security_manager.find_role(public_role)] if public_role else []
    return g.user.roles


def is_user_admin() -> bool:
    """当前用户是否管理员角色。"""
    user_roles = [role.name.lower() for role in list(get_user_roles())]
    return "admin" in user_roles


class BaseRabbitaiView(BaseView):
    """
    Rabbitai基础视图，扩展：BaseView，构造函数将注册视图中在Flask上公开的 Urls 为蓝图。

    定义以下属性：

    - appbuilder ：Web应用构建者
    - blueprint ：蓝图，调用 create_blueprint 方法创建。
    - endpoint ：终结点，默认为类名称 self.__class__.__name__
    - route_base ：路由基地址，如果要定义自己的相对url，请重写此选项，默认为：/ + self.__class__.__name__.lower()。
    - template_folder = "templates"：相对于应用的模板文件夹。
    - static_folder = "static"：相对于应用的静态资源文件夹。
    - base_permissions ：允许的基本权限的列表。
    - class_permission_name ：类权限名称，默认：self.__class__.__name__。
    - previous_class_permission_name ：如果设置安全性，则清除将删除具有此名称的所有权限元组。
    - method_permission_name ：各方法的权限。
    - previous_method_permission_name：与 method_permission_name 具有相同结构。如果设置了安全性，converge将用新的方法权限替换所有方法权限。
    - exclude_route_methods：要排除的路由方法集合。
    - include_route_methods：如果已定义，则将采用白名单设置，其中排除除在此属性上定义的端点之外的所有端点。
    - default_view = "list"：默认视图，url_for (method name)。
    - extra_args ：要注入到模板中的额外参数字典。
    - _apis ：API。

    传递 bootstrap_data（包括用户相关引导数据和通用引导数据）使用模板：rabbitai/spa.html。
    定义方法：json_response、render_app_template

    用户相关数据：

    - username
    - firstName
    - lastName
    - userId
    - isActive
    - createdOn
    - email
    - roles
    - permissions

    通用包括：

    - flash_messages
    - conf
    - locale
    - language_pack
    - feature_flags
    - menu_data
    - extra_sequential_color_schemes
    - extra_categorical_color_schemes
    - theme_overrides。

    """

    @staticmethod
    def json_response(obj: Any, status: int = 200) -> FlaskResponse:
        """
        返回Json格式响应对象。

        :param obj: 对象。
        :param status: 状态。
        :return:
        """

        return Response(
            json.dumps(obj, default=utils.json_int_dttm_ser, ignore_nan=True),
            status=status,
            mimetype="application/json",
        )

    def render_app_template(self) -> FlaskResponse:
        """
        渲染Html模板，返回 FlaskResponse。

        传递 bootstrap_data（包括用户相关引导数据和通用引导数据）使用模板：rabbitai/spa.html。

        :return:
        """

        payload = {
            "user": bootstrap_user_data(g.user, include_perms=True),
            "common": common_bootstrap_payload(),
        }
        return self.render_template(
            "rabbitai/spa.html",
            entry="spa",
            bootstrap_data=json.dumps(
                payload, default=utils.pessimistic_json_iso_dttm_ser
            ),
        )


def menu_data() -> Dict[str, Any]:
    """返回注册到应用程序构建者的菜单数据字典，包括：menu、brand、navbar_right。"""

    # 获取注册到应用构建者对象实例的菜单数据
    menu = appbuilder.menu.get_data()

    # 获取国际化语言
    languages = {}
    for lang in appbuilder.languages:
        languages[lang] = {
            **appbuilder.languages[lang],
            "url": appbuilder.get_url_for_locale(lang),
        }

    # 从应用配置对象中获取商标文本
    brand_text = appbuilder.app.config["LOGO_RIGHT_TEXT"]
    if callable(brand_text):
        brand_text = brand_text()

    return {
        "menu": menu,
        "brand": {
            "path": appbuilder.app.config["LOGO_TARGET_PATH"] or "/",
            "icon": appbuilder.app_icon,
            "alt": appbuilder.app_name,
            "width": appbuilder.app.config["APP_ICON_WIDTH"],
            "tooltip": appbuilder.app.config["LOGO_TOOLTIP"],
            "text": brand_text,
        },
        "navbar_right": {
            "show_watermark": ("rabbitai-logo-horiz" not in appbuilder.app_icon),
            "bug_report_url": appbuilder.app.config["BUG_REPORT_URL"],
            "documentation_url": appbuilder.app.config["DOCUMENTATION_URL"],
            "version_string": appbuilder.app.config["VERSION_STRING"],
            "version_sha": appbuilder.app.config["VERSION_SHA"],
            "languages": languages,
            "show_language_picker": len(languages.keys()) > 1,
            "user_is_anonymous": g.user.is_anonymous,
            "user_info_url": None
            if appbuilder.app.config["MENU_HIDE_USER_INFO"]
            else appbuilder.get_url_for_userinfo,
            "user_logout_url": appbuilder.get_url_for_logout,
            "user_login_url": appbuilder.get_url_for_login,
            "user_profile_url": None
            if g.user.is_anonymous or appbuilder.app.config["MENU_HIDE_USER_INFO"]
            else f"/rabbitai/profile/{g.user.username}",
            "locale": session.get("locale", "zh"),
        },
    }


def common_bootstrap_payload() -> Dict[str, Any]:
    """
    返回总是要发送到客户端的通用数据字典，

    至少包括：

    - flash_messages：快速信息。
    - conf：要发送到前端的配置字典。
    - locale：本地语言。
    - language_pack：语言包。
    - feature_flags：功能标志字典。
    - menu_data：菜单数据。
    - extra_sequential_color_schemes：自定义序列颜色方案。
    - extra_categorical_color_schemes：自定义类别颜色方案。
    - theme_overrides：主题。
    """

    messages = get_flashed_messages(with_categories=True)
    locale = str(get_locale())

    return {
        "flash_messages": messages,
        "conf": {k: conf.get(k) for k in FRONTEND_CONF_KEYS},
        "locale": locale,
        "language_pack": get_language_pack(locale),
        "feature_flags": get_feature_flags(),
        "extra_sequential_color_schemes": conf["EXTRA_SEQUENTIAL_COLOR_SCHEMES"],
        "extra_categorical_color_schemes": conf["EXTRA_CATEGORICAL_COLOR_SCHEMES"],
        "theme_overrides": conf["THEME_OVERRIDES"],
        "menu_data": menu_data(),
    }

# region 错误处理


# pylint: disable=invalid-name
def get_error_level_from_status_code(status: int) -> ErrorLevel:
    if status < 400:
        return ErrorLevel.INFO
    if status < 500:
        return ErrorLevel.WARNING
    return ErrorLevel.ERROR


# SIP-40 compatible error responses; make sure APIs raise
# RabbitaiErrorException or RabbitaiErrorsException
@rabbitai_app.errorhandler(RabbitaiErrorException)
def show_rabbitai_error(ex: RabbitaiErrorException) -> FlaskResponse:
    logger.warning(ex)
    return json_errors_response(errors=[ex.error], status=ex.status)


@rabbitai_app.errorhandler(RabbitaiErrorsException)
def show_rabbitai_errors(ex: RabbitaiErrorsException) -> FlaskResponse:
    logger.warning(ex)
    return json_errors_response(errors=ex.errors, status=ex.status)


# Redirect to login if the CSRF token is expired
@rabbitai_app.errorhandler(CSRFError)
def refresh_csrf_token(ex: CSRFError) -> FlaskResponse:
    """处理 CSRFError 的回调函数。"""
    logger.warning(ex)

    if request.is_json:
        return show_http_exception(ex)

    return redirect(appbuilder.get_url_for_login)


@rabbitai_app.errorhandler(HTTPException)
def show_http_exception(ex: HTTPException) -> FlaskResponse:
    """处理 HTTPException 错误的回调。"""
    logger.warning(ex)
    if (
        "text/html" in request.accept_mimetypes
        and not config["DEBUG"]
        and ex.code in {404, 500}
    ):
        path = resource_filename("rabbitai", f"static/assets/{ex.code}.html")
        return send_file(path), ex.code

    return json_errors_response(
        errors=[
            RabbitaiError(
                message=utils.error_msg_from_exception(ex),
                error_type=RabbitaiErrorType.GENERIC_BACKEND_ERROR,
                level=ErrorLevel.ERROR,
            ),
        ],
        status=ex.code or 500,
    )


# Temporary handler for CommandException; if an API raises a
# CommandException it should be fixed to map it to RabbitaiErrorException
# or RabbitaiErrorsException, with a specific status code and error type
@rabbitai_app.errorhandler(CommandException)
def show_command_errors(ex: CommandException) -> FlaskResponse:
    """应用错误处理查询，显示命令错误。"""
    logger.warning(ex)
    extra = ex.normalized_messages() if isinstance(ex, CommandInvalidError) else {}
    return json_errors_response(
        errors=[
            RabbitaiError(
                message=ex.message,
                error_type=RabbitaiErrorType.GENERIC_COMMAND_ERROR,
                level=get_error_level_from_status_code(ex.status),
                extra=extra,
            ),
        ],
        status=ex.status,
    )


# Catch-all, to ensure all errors from the backend conform to SIP-40
@rabbitai_app.errorhandler(Exception)
def show_unexpected_exception(ex: Exception) -> FlaskResponse:
    """应用错误处理查询，显示未知错误。"""

    logger.exception(ex)
    return json_errors_response(
        errors=[
            RabbitaiError(
                message=utils.error_msg_from_exception(ex),
                error_type=RabbitaiErrorType.GENERIC_BACKEND_ERROR,
                level=ErrorLevel.ERROR,
            ),
        ],
    )

# endregion


@rabbitai_app.context_processor
def get_common_bootstrap_data() -> Dict[str, Any]:
    """注册为模板上下文处理器，获取通用引导数据 bootstrap_data，并作为模板数据传递到模板。"""

    def serialize_bootstrap_data() -> str:
        """序列化引导数据。"""
        return json.dumps(
            {"common": common_bootstrap_payload()},
            default=utils.pessimistic_json_iso_dttm_ser,
        )

    return {"bootstrap_data": serialize_bootstrap_data}


class RabbitaiListWidget(ListWidget):
    """RabbitAI列表部件，扩展：ListWidget，基于模板：rabbitai/fab_overrides/list.html。"""

    template = "rabbitai/fab_overrides/list.html"


class RabbitaiModelView(ModelView):
    """
    Rabbitai模型视图，扩展：ModelView，实现CRUD功能，

    传递 bootstrap_data（包括用户相关数据和通用数据）使用模板：rabbitai/spa.html。

    用户相关数据：

    - username
    - firstName
    - lastName
    - userId
    - isActive
    - createdOn
    - email
    - roles
    - permissions

    通用包括：

    - flash_messages
    - conf
    - locale
    - language_pack
    - feature_flags
    - menu_data
    - extra_sequential_color_schemes
    - extra_categorical_color_schemes
    - theme_overrides。

    """

    page_size = 100
    """页面大小，默认100"""
    list_widget = RabbitaiListWidget
    """显示列表的部件"""

    def render_app_template(self) -> FlaskResponse:
        """
        渲染Html模板，返回 FlaskResponse。

        传递 bootstrap_data（包括用户相关引导数据和通用引导数据）使用模板：rabbitai/spa.html。

        :return: FlaskResponse。
        """

        payload = {
            "user": bootstrap_user_data(g.user, include_perms=True),
            "common": common_bootstrap_payload(),
        }
        return self.render_template(
            "rabbitai/spa.html",
            entry="spa",
            bootstrap_data=json.dumps(
                payload, default=utils.pessimistic_json_iso_dttm_ser
            ),
        )


class ListWidgetWithCheckboxes(ListWidget):
    """
    An alternative to list view that renders Boolean fields as checkboxes

    Works in conjunction with the `checkbox` view."""

    template = "rabbitai/fab_overrides/list_with_checkboxes.html"


def validate_json(form: Form, field: Field) -> None:
    """
    验证指定字段的数据是否Json对象格式，如果不是则引发异常。

    :param form:
    :param field:
    :return:
    """

    try:
        json.loads(field.data)
    except Exception as ex:
        logger.exception(ex)
        raise Exception(_("json isn't valid"))


class YamlExportMixin:
    """
    导出为 YAML 文件混入类，提供将数据导出为 YAML 格式文件的功能。
    """

    yaml_dict_key: Optional[str] = None

    @action("yaml_export", __("Export to YAML"), __("Export to YAML?"), "fa-download")
    def yaml_export(
        self, items: Union[ImportExportMixin, List[ImportExportMixin]]
    ) -> FlaskResponse:
        if not isinstance(items, list):
            items = [items]

        data = [t.export_to_dict() for t in items]

        return Response(
            yaml.safe_dump({self.yaml_dict_key: data} if self.yaml_dict_key else data),
            headers=generate_download_headers("yaml"),
            mimetype="application/text",
        )


class DeleteMixin:
    """删除混入类，提供批量删除对象关系模型的操作，并公开操作：muldelete。"""

    def _delete(self: BaseView, primary_key: int) -> None:
        """
        Delete function logic, override to implement diferent logic
        deletes the record with primary_key = primary_key

        :param primary_key:
            record primary key to delete
        """
        item = self.datamodel.get(primary_key, self._base_filters)
        if not item:
            abort(404)
        try:
            self.pre_delete(item)
        except Exception as ex:  # pylint: disable=broad-except
            flash(str(ex), "danger")
        else:
            view_menu = security_manager.find_view_menu(item.get_perm())
            pvs = (
                security_manager.get_session.query(
                    security_manager.permissionview_model
                )
                .filter_by(view_menu=view_menu)
                .all()
            )

            if self.datamodel.delete(item):
                self.post_delete(item)

                for pv in pvs:
                    security_manager.get_session.delete(pv)

                if view_menu:
                    security_manager.get_session.delete(view_menu)

                security_manager.get_session.commit()

            flash(*self.datamodel.message)
            self.update_redirect()

    @action(
        "muldelete", __("Delete"), __("Delete all Really?"), "fa-trash", single=False
    )
    def muldelete(self: BaseView, items: List[Model]) -> FlaskResponse:
        if not items:
            abort(404)
        for item in items:
            try:
                self.pre_delete(item)
            except Exception as ex:  # pylint: disable=broad-except
                flash(str(ex), "danger")
            else:
                self._delete(item.id)

        self.update_redirect()

        return redirect(self.get_redirect())


class DatasourceFilter(BaseFilter):
    """数据源过滤器，依据访问权限过滤可以访问的数据。"""

    def apply(self, query: Query, value: Any) -> Query:
        if security_manager.can_access_all_datasources():
            return query
        datasource_perms = security_manager.user_view_menu_names("datasource_access")
        schema_perms = security_manager.user_view_menu_names("schema_access")
        return query.filter(
            or_(
                self.model.perm.in_(datasource_perms),
                self.model.schema_perm.in_(schema_perms),
            )
        )


class CsvResponse(Response):
    """依据 config.py 指定的编码配置CVS响应。"""

    charset = conf["CSV_EXPORT"].get("encoding", "utf-8")
    default_mimetype = "text/csv"


def check_ownership(obj: Any, raise_if_false: bool = True) -> bool:
    """
    检查拥有者。

    在 `pre_update` 回调中用于强制拥有者检查。

    Admin have all access, and other users need to be referenced on either
    the created_by field that comes with the ``AuditMixin``, or in a field
    named ``owners`` which is expected to be a one-to-many with the User
    model. It is meant to be used in the ModelView's pre_update hook in
    which raising will abort the update.
    """

    if not obj:
        return False

    security_exception = RabbitaiSecurityException(
        RabbitaiError(
            error_type=RabbitaiErrorType.MISSING_OWNERSHIP_ERROR,
            message="You don't have the rights to alter [{}]".format(obj),
            level=ErrorLevel.ERROR,
        )
    )

    if g.user.is_anonymous:
        if raise_if_false:
            raise security_exception
        return False
    if is_user_admin():
        return True
    scoped_session = db.create_scoped_session()
    orig_obj = scoped_session.query(obj.__class__).filter_by(id=obj.id).first()

    # Making a list of owners that works across ORM models
    owners: List[User] = []
    if hasattr(orig_obj, "owners"):
        owners += orig_obj.owners
    if hasattr(orig_obj, "owner"):
        owners += [orig_obj.owner]
    if hasattr(orig_obj, "created_by"):
        owners += [orig_obj.created_by]

    owner_names = [o.username for o in owners if o]

    if g.user and hasattr(g.user, "username") and g.user.username in owner_names:
        return True
    if raise_if_false:
        raise security_exception
    return False


def bind_field(
    _: Any, form: DynamicForm, unbound_field: UnboundField, options: Dict[Any, Any]
) -> Field:
    """
    通过去除所有空白来自定义字段的绑定方式。

    :param form: 表单。
    :param unbound_field: 未绑定字段。
    :param options: 字段选项字典。
    :returns: 绑定字段。
    """

    filters = unbound_field.kwargs.get("filters", [])
    filters.append(lambda x: x.strip() if isinstance(x, str) else x)
    return unbound_field.bind(form=form, filters=filters, **options)


FlaskForm.Meta.bind_field = bind_field


@rabbitai_app.after_request
def apply_http_headers(response: Response) -> Response:
    """每次请求后要调用的方法，应用配置的Http标头到响应对象。"""

    # HTTP_HEADERS is deprecated, this provides backwards compatibility
    response.headers.extend(
        {**config["OVERRIDE_HTTP_HEADERS"], **config["HTTP_HEADERS"]}
    )

    for k, v in config["DEFAULT_HTTP_HEADERS"].items():
        if k not in response.headers:
            response.headers[k] = v

    return response
