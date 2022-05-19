# -*- coding: utf-8 -*-

"""权限和安全性管理相关的常量和方法集合。"""

import logging
import re
from collections import defaultdict
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from flask import current_app, g
from flask_appbuilder import Model
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.sqla.models import (
    assoc_permissionview_role,
    assoc_user_role,
    PermissionView,
    Role,
    User,
)
from flask_appbuilder.security.views import (
    PermissionModelView,
    PermissionViewModelView,
    RoleModelView,
    UserModelView,
    ViewMenuModelView,
)
from flask_appbuilder.widgets import ListWidget
from flask_login import AnonymousUserMixin
from sqlalchemy import and_, or_
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.query import Query as SqlaQuery

from rabbitai import sql_parse
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.constants import RouteMethod
from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import RabbitaiSecurityException
from rabbitai.utils.core import DatasourceName, RowLevelSecurityFilterType

if TYPE_CHECKING:
    from rabbitai.common.query_context import QueryContext
    from rabbitai.connectors.base.models import BaseDatasource
    from rabbitai.connectors.druid.models import DruidCluster
    from rabbitai.models.dashboard import Dashboard
    from rabbitai.models.core import Database
    from rabbitai.models.sql_lab import Query
    from rabbitai.sql_parse import Table
    from rabbitai.viz import BaseViz

logger = logging.getLogger(__name__)


class RabbitaiSecurityListWidget(ListWidget):
    """安全列表部件，模板：rabbitai/fab_overrides/list.html。"""

    template = "rabbitai/fab_overrides/list.html"


class RabbitaiRoleListWidget(ListWidget):
    """角色列表部件，模板：rabbitai/fab_overrides/list_role.html"""

    template = "rabbitai/fab_overrides/list_role.html"

    def __init__(self, **kwargs: Any) -> None:
        kwargs["appbuilder"] = current_app.appbuilder
        super().__init__(**kwargs)


# 指定安全相关视图显示列表的部件
UserModelView.list_widget = RabbitaiSecurityListWidget
RoleModelView.list_widget = RabbitaiRoleListWidget
PermissionViewModelView.list_widget = RabbitaiSecurityListWidget
PermissionModelView.list_widget = RabbitaiSecurityListWidget

# 指定各安全相关视图的路由方法
UserModelView.include_route_methods = RouteMethod.CRUD_SET | {
    RouteMethod.ACTION,
    RouteMethod.API_READ,
    RouteMethod.ACTION_POST,
    "userinfo",
}
RoleModelView.include_route_methods = RouteMethod.CRUD_SET
PermissionViewModelView.include_route_methods = {RouteMethod.LIST}
PermissionModelView.include_route_methods = {RouteMethod.LIST}
ViewMenuModelView.include_route_methods = {RouteMethod.LIST}

RoleModelView.list_columns = ["name"]
RoleModelView.edit_columns = ["name", "permissions", "user"]
RoleModelView.related_views = []


class RabbitaiSecurityManager(SecurityManager):
    """
    RabbitAI 安全管理器，扩展：SecurityManager。

    负责身份验证、注册安全视图、角色和权限自动管理，
    如果要更改任何内容，只需继承和重写，然后将自己的安全管理器传递给AppBuilder。
    """

    # region 类属性

    userstatschartview = None
    """用户统计图表视图，默认None"""

    READ_ONLY_MODEL_VIEWS = {"Database", "DruidClusterModelView", "DynamicPlugin"}
    """只读模型视图名称集合，Database、DruidClusterModelView、DynamicPlugin"""

    USER_MODEL_VIEWS = {
        "UserDBModelView",
        "UserLDAPModelView",
        "UserOAuthModelView",
        "UserOIDModelView",
        "UserRemoteUserModelView",
    }
    """用户模型视图名称集合，UserDBModelView、UserLDAPModelView、UserOAuthModelView、UserRemoteUserModelView"""

    GAMMA_READ_ONLY_MODEL_VIEWS = {
                                      "Dataset",
                                      "DruidColumnInlineView",
                                      "DruidDatasourceModelView",
                                      "DruidMetricInlineView",
                                      "Datasource",
                                  } | READ_ONLY_MODEL_VIEWS
    """GAMMA类型角色只读模型视图名称集合，
    Dataset、DruidColumnInlineView、DruidDatasourceModelView、DruidMetricInlineView、Datasource"""

    ADMIN_ONLY_VIEW_MENUS = {
                                "AccessRequestsModelView",
                                "SQL Lab",
                                "Refresh Druid Metadata",
                                "ResetPasswordView",
                                "RoleModelView",
                                "Log",
                                "Security",
                                "Row Level Security",
                                "Row Level Security Filters",
                                "RowLevelSecurityFiltersModelView",
                            } | USER_MODEL_VIEWS
    """管理员视图菜单名称的集合。"""

    ALPHA_ONLY_VIEW_MENUS = {
        "Manage",
        "CSS Templates",
        "Queries",
        "Import dashboards",
        "Upload a CSV",
    }
    """ALPHA视图菜单名称的集合。"""
    ADMIN_ONLY_PERMISSIONS = {
        "can_sql_json",
        "can_override_role_permissions",
        "can_sync_druid_source",
        "can_override_role_permissions",
        "can_approve",
        "can_update_role",
        "all_query_access",
    }
    """管理员权限名称的集合。"""
    READ_ONLY_PERMISSION = {
        "can_show",
        "can_list",
        "can_get",
        "can_external_metadata",
        "can_external_metadata_by_name",
        "can_read",
    }
    """只读权限名称的集合。"""
    ALPHA_ONLY_PERMISSIONS = {
        "muldelete",
        "all_database_access",
        "all_datasource_access",
    }
    """ALPHA权限名称的集合。"""
    OBJECT_SPEC_PERMISSIONS = {
        "database_access",
        "schema_access",
        "datasource_access",
        "metric_access",
    }
    """对象规范权限名称的集合。"""

    ACCESSIBLE_PERMS = {"can_userinfo", "resetmypassword"}
    """可访问权限名称集合"""
    SQLLAB_PERMISSION_VIEWS = {
        ("can_csv", "Rabbitai"),
        ("can_read", "SavedQuery"),
        ("can_read", "Database"),
        ("can_sql_json", "Rabbitai"),
        ("can_sqllab_viz", "Rabbitai"),
        ("can_sqllab_table_viz", "Rabbitai"),
        ("can_sqllab", "Rabbitai"),
        ("menu_access", "SQL Lab"),
        ("menu_access", "SQL Editor"),
        ("menu_access", "Saved Queries"),
        ("menu_access", "Query Search"),
    }
    """SQLLAB权限视图集合"""

    data_access_permissions = (
        "database_access",
        "schema_access",
        "datasource_access",
        "all_datasource_access",
        "all_database_access",
        "all_query_access",
    )
    """数据访问权限列表"""

    # endregion

    def get_schema_perm(
        self, database: Union["Database", str], schema: Optional[str] = None
    ) -> Optional[str]:
        """
        返回数据库模式权限，格式[{database}].[{schema}] 或None。

        :param database: 数据库或数据库名称。
        :param schema: 模式名称
        :return: 数据库模式权限。
        """

        if schema:
            return f"[{database}].[{schema}]"

        return None

    def unpack_schema_perm(self, schema_permission: str) -> Tuple[str, str]:
        """
        分解指定数据库模式权限为数据库名称和模式名称的元组。

        :param schema_permission: 数据库模式权限，[database_name].[schema_name]
        :return:
        """

        # [database_name].[schema_name]
        schema_name = schema_permission.split(".")[1][1:-1]
        database_name = schema_permission.split(".")[0][1:-1]
        return database_name, schema_name

    def can_access(self, permission_name: str, view_name: str) -> bool:
        """
        Return True if the user can access the FAB permission/view, False otherwise.

        Note this method adds protection from has_access failing from missing
        permission/view entries.

        :param permission_name: The FAB permission name
        :param view_name: The FAB view-menu name
        :returns: Whether the user can access the FAB permission/view
        """

        user = g.user
        if user.is_anonymous:
            return self.is_item_public(permission_name, view_name)
        return self._has_view_access(user, permission_name, view_name)

    def can_access_all_queries(self) -> bool:
        """
        Return True if the user can access all SQL Lab queries, False otherwise.

        :returns: Whether the user can access all queries
        """

        return self.can_access("all_query_access", "all_query_access")

    def can_access_all_datasources(self) -> bool:
        """
        Return True if the user can fully access all the Rabbitai datasources, False
        otherwise.

        :returns: Whether the user can fully access all Rabbitai datasources
        """

        return self.can_access("all_datasource_access", "all_datasource_access")

    def can_access_all_databases(self) -> bool:
        """
        Return True if the user can fully access all the Rabbitai databases, False
        otherwise.

        :returns: Whether the user can fully access all Rabbitai databases
        """

        return self.can_access("all_database_access", "all_database_access")

    def can_access_database(self, database: Union["Database", "DruidCluster"]) -> bool:
        """
        Return True if the user can fully access the Rabbitai database, False otherwise.

        Note for Druid the database is akin to the Druid cluster.

        :param database: The Rabbitai database
        :returns: Whether the user can fully access the Rabbitai database
        """

        return (
            self.can_access_all_datasources()
            or self.can_access_all_databases()
            or self.can_access("database_access", database.perm)  # type: ignore
        )

    def can_access_schema(self, datasource: "BaseDatasource") -> bool:
        """
        Return True if the user can fully access the schema associated with the Rabbitai
        datasource, False otherwise.

        Note for Druid datasources the database and schema are akin to the Druid cluster
        and datasource name prefix respectively, i.e., [schema.]datasource.

        :param datasource: The Rabbitai datasource
        :returns: Whether the user can fully access the datasource's schema
        """

        return (
            self.can_access_all_datasources()
            or self.can_access_database(datasource.database)
            or self.can_access("schema_access", datasource.schema_perm or "")
        )

    def can_access_datasource(self, datasource: "BaseDatasource") -> bool:
        """
        Return True if the user can fully access of the Rabbitai datasource, False
        otherwise.

        :param datasource: The Rabbitai datasource
        :returns: Whether the user can fully access the Rabbitai datasource
        """

        try:
            self.raise_for_access(datasource=datasource)
        except RabbitaiSecurityException:
            return False

        return True

    @staticmethod
    def get_datasource_access_error_msg(datasource: "BaseDatasource") -> str:
        """
        Return the error message for the denied Rabbitai datasource.

        :param datasource: The denied Rabbitai datasource
        :returns: The error message
        """

        return f"""This endpoint requires the datasource {datasource.name}, database or
            `all_datasource_access` permission"""

    @staticmethod
    def get_datasource_access_link(datasource: "BaseDatasource", ) -> Optional[str]:
        """
        Return the link for the denied Rabbitai datasource.

        :param datasource: The denied Rabbitai datasource
        :returns: The access URL
        """

        from rabbitai import conf

        return conf.get("PERMISSION_INSTRUCTIONS_LINK")

    def get_datasource_access_error_object(self, datasource: "BaseDatasource") -> RabbitaiError:
        """
        Return the error object for the denied Rabbitai datasource.

        :param datasource: The denied Rabbitai datasource
        :returns: The error object
        """
        return RabbitaiError(
            error_type=RabbitaiErrorType.DATASOURCE_SECURITY_ACCESS_ERROR,
            message=self.get_datasource_access_error_msg(datasource),
            level=ErrorLevel.ERROR,
            extra={
                "link": self.get_datasource_access_link(datasource),
                "datasource": datasource.name,
            },
        )

    def get_table_access_error_msg(self, tables: Set["Table"]) -> str:
        """
        Return the error message for the denied SQL tables.

        :param tables: The set of denied SQL tables
        :returns: The error message
        """

        quoted_tables = [f"`{table}`" for table in tables]
        return f"""You need access to the following tables: {", ".join(quoted_tables)},
            `all_database_access` or `all_datasource_access` permission"""

    def get_table_access_error_object(self, tables: Set["Table"]) -> RabbitaiError:
        """
        Return the error object for the denied SQL tables.

        :param tables: The set of denied SQL tables
        :returns: The error object
        """
        return RabbitaiError(
            error_type=RabbitaiErrorType.TABLE_SECURITY_ACCESS_ERROR,
            message=self.get_table_access_error_msg(tables),
            level=ErrorLevel.ERROR,
            extra={
                "link": self.get_table_access_link(tables),
                "tables": [str(table) for table in tables],
            },
        )

    def get_table_access_link(self, tables: Set["Table"]) -> Optional[str]:
        """
        Return the access link for the denied SQL tables.

        :param tables: The set of denied SQL tables
        :returns: The access URL
        """

        from rabbitai import conf

        return conf.get("PERMISSION_INSTRUCTIONS_LINK")

    def get_user_datasources(self) -> List["BaseDatasource"]:
        """
        Collect datasources which the user has explicit permissions to.

        :returns: The list of datasources
        """

        user_perms = self.user_view_menu_names("datasource_access")
        schema_perms = self.user_view_menu_names("schema_access")
        user_datasources = set()
        for datasource_class in ConnectorRegistry.sources.values():
            user_datasources.update(
                self.get_session.query(datasource_class)
                    .filter(
                    or_(
                        datasource_class.perm.in_(user_perms),
                        datasource_class.schema_perm.in_(schema_perms),
                    )
                )
                    .all()
            )

        # group all datasources by database
        all_datasources = ConnectorRegistry.get_all_datasources(self.get_session)
        datasources_by_database: Dict["Database", Set["BaseDatasource"]] = defaultdict(
            set
        )
        for datasource in all_datasources:
            datasources_by_database[datasource.database].add(datasource)

        # add datasources with implicit permission (eg, database access)
        for database, datasources in datasources_by_database.items():
            if self.can_access_database(database):
                user_datasources.update(datasources)

        return list(user_datasources)

    def can_access_table(self, database: "Database", table: "Table") -> bool:
        """
        Return True if the user can access the SQL table, False otherwise.

        :param database: The SQL database
        :param table: The SQL table
        :returns: Whether the user can access the SQL table
        """

        try:
            self.raise_for_access(database=database, table=table)
        except RabbitaiSecurityException:
            return False

        return True

    def user_view_menu_names(self, permission_name: str) -> Set[str]:
        """
        返回用户可以访问的视图菜单名称的列表。

        :param permission_name: 权限名称。
        :return:
        """

        base_query = (
            self.get_session.query(self.viewmenu_model.name)
                .join(self.permissionview_model)
                .join(self.permission_model)
                .join(assoc_permissionview_role)
                .join(self.role_model)
        )

        if not g.user.is_anonymous:
            # filter by user id
            view_menu_names = (
                base_query.join(assoc_user_role)
                    .join(self.user_model)
                    .filter(self.user_model.id == g.user.get_id())
                    .filter(self.permission_model.name == permission_name)
            ).all()

            return {s.name for s in view_menu_names}

        # Properly treat anonymous user
        public_role = self.get_public_role()
        if public_role:
            # filter by public role
            view_menu_names = (
                base_query.filter(self.role_model.id == public_role.id).filter(
                    self.permission_model.name == permission_name
                )
            ).all()
            return {s.name for s in view_menu_names}
        return set()

    def get_schemas_accessible_by_user(
        self, database: "Database", schemas: List[str], hierarchical: bool = True
    ) -> List[str]:
        """
        Return the list of SQL schemas accessible by the user.

        :param database: The SQL database
        :param schemas: The list of eligible SQL schemas
        :param hierarchical: Whether to check using the hierarchical permission logic
        :returns: The list of accessible SQL schemas
        """

        from rabbitai.connectors.sqla.models import SqlaTable

        if hierarchical and self.can_access_database(database):
            return schemas

        # schema_access
        accessible_schemas = {
            self.unpack_schema_perm(s)[1]
            for s in self.user_view_menu_names("schema_access")
            if s.startswith(f"[{database}].")
        }

        # datasource_access
        perms = self.user_view_menu_names("datasource_access")
        if perms:
            tables = (
                self.get_session.query(SqlaTable.schema)
                    .filter(SqlaTable.database_id == database.id)
                    .filter(SqlaTable.schema.isnot(None))
                    .filter(SqlaTable.schema != "")
                    .filter(or_(SqlaTable.perm.in_(perms)))
                    .distinct()
            )
            accessible_schemas.update([table.schema for table in tables])

        return [s for s in schemas if s in accessible_schemas]

    def get_datasources_accessible_by_user(
        self,
        database: "Database",
        datasource_names: List[DatasourceName],
        schema: Optional[str] = None,
    ) -> List[DatasourceName]:
        """
        Return the list of SQL tables accessible by the user.

        :param database: The SQL database
        :param datasource_names: The list of eligible SQL tables w/ schema
        :param schema: The fallback SQL schema if not present in the table name
        :returns: The list of accessible SQL tables w/ schema
        """

        if self.can_access_database(database):
            return datasource_names

        if schema:
            schema_perm = self.get_schema_perm(database, schema)
            if schema_perm and self.can_access("schema_access", schema_perm):
                return datasource_names

        user_perms = self.user_view_menu_names("datasource_access")
        schema_perms = self.user_view_menu_names("schema_access")
        user_datasources = ConnectorRegistry.query_datasources_by_permissions(
            self.get_session, database, user_perms, schema_perms
        )
        if schema:
            names = {d.table_name for d in user_datasources if d.schema == schema}
            return [d for d in datasource_names if d in names]

        full_names = {d.full_name for d in user_datasources}
        return [d for d in datasource_names if f"[{database}].[{d}]" in full_names]

    def merge_perm(self, permission_name: str, view_menu_name: str) -> None:
        """
        Add the FAB permission/view-menu.

        :param permission_name: The FAB permission name
        :param view_menu_names: The FAB view-menu name
        :see: SecurityManager.add_permission_view_menu
        """

        logger.warning(
            "This method 'merge_perm' is deprecated use add_permission_view_menu"
        )
        self.add_permission_view_menu(permission_name, view_menu_name)

    def _is_user_defined_permission(self, perm: Model) -> bool:
        """
        Return True if the FAB permission is user defined, False otherwise.

        :param perm: The FAB permission
        :returns: Whether the FAB permission is user defined
        """

        return perm.permission.name in self.OBJECT_SPEC_PERMISSIONS

    def create_custom_permissions(self) -> None:
        """
        Create custom FAB permissions.
        """
        self.add_permission_view_menu("all_datasource_access", "all_datasource_access")
        self.add_permission_view_menu("all_database_access", "all_database_access")
        self.add_permission_view_menu("all_query_access", "all_query_access")
        self.add_permission_view_menu("can_share_dashboard", "Rabbitai")
        self.add_permission_view_menu("can_share_chart", "Rabbitai")

    def create_missing_perms(self) -> None:
        """
        Creates missing FAB permissions for datasources, schemas and metrics.
        """

        from rabbitai.models import core as models

        logger.info("Fetching a set of all perms to lookup which ones are missing")
        all_pvs = set()
        for pv in self.get_session.query(self.permissionview_model).all():
            if pv.permission and pv.view_menu:
                all_pvs.add((pv.permission.name, pv.view_menu.name))

        def merge_pv(view_menu: str, perm: str) -> None:
            """Create permission view menu only if it doesn't exist"""
            if view_menu and perm and (view_menu, perm) not in all_pvs:
                self.add_permission_view_menu(view_menu, perm)

        logger.info("Creating missing datasource permissions.")
        datasources = ConnectorRegistry.get_all_datasources(self.get_session)
        for datasource in datasources:
            merge_pv("datasource_access", datasource.get_perm())
            merge_pv("schema_access", datasource.get_schema_perm())

        logger.info("Creating missing database permissions.")
        databases = self.get_session.query(models.Database).all()
        for database in databases:
            merge_pv("database_access", database.perm)

    def clean_perms(self) -> None:
        """
        Clean up the FAB faulty permissions.
        """

        logger.info("Cleaning faulty perms")
        sesh = self.get_session
        pvms = sesh.query(PermissionView).filter(
            or_(
                PermissionView.permission is None,  # == None
                PermissionView.view_menu is None,   # == None
            )
        )
        deleted_count = pvms.delete()
        sesh.commit()
        if deleted_count:
            logger.info("Deleted %i faulty permissions", deleted_count)

    def sync_role_definitions(self) -> None:
        """
        Initialize the Rabbitai application with security roles and such.
        """

        from rabbitai import conf

        logger.info("Syncing role definition")

        self.create_custom_permissions()

        # Creating default roles
        self.set_role("Admin", self._is_admin_pvm)
        self.set_role("Alpha", self._is_alpha_pvm)
        self.set_role("Gamma", self._is_gamma_pvm)
        self.set_role("granter", self._is_granter_pvm)
        self.set_role("sql_lab", self._is_sql_lab_pvm)

        # Configure public role
        if conf["PUBLIC_ROLE_LIKE"]:
            self.copy_role(conf["PUBLIC_ROLE_LIKE"], self.auth_role_public, merge=True)
        if conf.get("PUBLIC_ROLE_LIKE_GAMMA", False):
            logger.warning(
                "The config `PUBLIC_ROLE_LIKE_GAMMA` is deprecated and will be removed "
                "in Rabbitai 1.0. Please use `PUBLIC_ROLE_LIKE` instead."
            )
            self.copy_role("Gamma", self.auth_role_public, merge=True)

        self.create_missing_perms()

        # commit role and view menu updates
        self.get_session.commit()
        self.clean_perms()

    def _get_pvms_from_builtin_role(self, role_name: str) -> List[PermissionView]:
        """
        Gets a list of model PermissionView permissions infered from a builtin role
        definition
        """
        role_from_permissions_names = self.builtin_roles.get(role_name, [])
        all_pvms = self.get_session.query(PermissionView).all()
        role_from_permissions = []
        for pvm_regex in role_from_permissions_names:
            view_name_regex = pvm_regex[0]
            permission_name_regex = pvm_regex[1]
            for pvm in all_pvms:
                if re.match(view_name_regex, pvm.view_menu.name) and re.match(
                    permission_name_regex, pvm.permission.name
                ):
                    if pvm not in role_from_permissions:
                        role_from_permissions.append(pvm)
        return role_from_permissions

    def find_roles_by_id(self, role_ids: List[int]) -> List[Role]:
        """
        Find a List of models by a list of ids, if defined applies `base_filter`
        """
        query = self.get_session.query(Role).filter(Role.id.in_(role_ids))
        return query.all()

    def copy_role(self, role_from_name: str, role_to_name: str, merge: bool = True) -> None:
        """
        Copies permissions from a role to another.

        Note: Supports regex defined builtin roles

        :param role_from_name: The FAB role name from where the permissions are taken
        :param role_to_name: The FAB role name from where the permissions are copied to
        :param merge: If merge is true, keep data access permissions
            if they already exist on the target role
        """

        logger.info("Copy/Merge %s to %s", role_from_name, role_to_name)
        # If it's a builtin role extract permissions from it
        if role_from_name in self.builtin_roles:
            role_from_permissions = self._get_pvms_from_builtin_role(role_from_name)
        else:
            role_from_permissions = list(self.find_role(role_from_name).permissions)
        role_to = self.add_role(role_to_name)
        # If merge, recover existing data access permissions
        if merge:
            for permission_view in role_to.permissions:
                if (
                    permission_view not in role_from_permissions
                    and permission_view.permission.name in self.data_access_permissions
                ):
                    role_from_permissions.append(permission_view)
        role_to.permissions = role_from_permissions
        self.get_session.merge(role_to)
        self.get_session.commit()

    def set_role(self, role_name: str, pvm_check: Callable[[PermissionView], bool]) -> None:
        """
        Set the FAB permission/views for the role.

        :param role_name: The FAB role name
        :param pvm_check: The FAB permission/view check
        """

        logger.info("Syncing %s perms", role_name)
        pvms = self.get_session.query(PermissionView).all()
        pvms = [p for p in pvms if p.permission and p.view_menu]
        role = self.add_role(role_name)
        role_pvms = [
            permission_view for permission_view in pvms if pvm_check(permission_view)
        ]
        role.permissions = role_pvms
        self.get_session.merge(role)
        self.get_session.commit()

    def _is_admin_only(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is accessible to only Admin users,
        False otherwise.

        Note readonly operations on read only model views are allowed only for admins.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is accessible to only Admin users
        """

        if (
            pvm.view_menu.name in self.READ_ONLY_MODEL_VIEWS
            and pvm.permission.name not in self.READ_ONLY_PERMISSION
        ):
            return True
        return (
            pvm.view_menu.name in self.ADMIN_ONLY_VIEW_MENUS
            or pvm.permission.name in self.ADMIN_ONLY_PERMISSIONS
        )

    def _is_alpha_only(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is accessible to only Alpha users,
        False otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is accessible to only Alpha users
        """

        if (
            pvm.view_menu.name in self.GAMMA_READ_ONLY_MODEL_VIEWS
            and pvm.permission.name not in self.READ_ONLY_PERMISSION
        ):
            return True
        return (
            pvm.view_menu.name in self.ALPHA_ONLY_VIEW_MENUS
            or pvm.permission.name in self.ALPHA_ONLY_PERMISSIONS
        )

    def _is_accessible_to_all(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is accessible to all, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is accessible to all users
        """

        return pvm.permission.name in self.ACCESSIBLE_PERMS

    def _is_admin_pvm(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is Admin user related, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is Admin related
        """

        return not self._is_user_defined_permission(pvm)

    def _is_alpha_pvm(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is Alpha user related, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is Alpha related
        """

        return not (
            self._is_user_defined_permission(pvm) or self._is_admin_only(pvm)
        ) or self._is_accessible_to_all(pvm)

    def _is_gamma_pvm(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is Gamma user related, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is Gamma related
        """

        return not (
            self._is_user_defined_permission(pvm)
            or self._is_admin_only(pvm)
            or self._is_alpha_only(pvm)
        ) or self._is_accessible_to_all(pvm)

    def _is_sql_lab_pvm(self, pvm: PermissionView) -> bool:
        """
        Return True if the FAB permission/view is SQL Lab related, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the FAB object is SQL Lab related
        """
        return (pvm.permission.name, pvm.view_menu.name) in self.SQLLAB_PERMISSION_VIEWS

    def _is_granter_pvm(self, pvm: PermissionView) -> bool:
        """
        Return True if the user can grant the FAB permission/view, False
        otherwise.

        :param pvm: The FAB permission/view
        :returns: Whether the user can grant the FAB permission/view
        """

        return pvm.permission.name in {"can_override_role_permissions", "can_approve"}

    def set_perm(self, mapper: Mapper, connection: Connection, target: "BaseDatasource") -> None:
        """
        Set the datasource permissions.

        :param mapper: The table mapper
        :param connection: The DB-API connection
        :param target: The mapped instance being persisted
        """
        link_table = target.__table__  # pylint: disable=no-member
        if target.perm != target.get_perm():
            connection.execute(
                link_table.update()
                    .where(link_table.c.id == target.id)
                    .values(perm=target.get_perm())
            )

        if (
            hasattr(target, "schema_perm")
            and target.schema_perm != target.get_schema_perm()
        ):
            connection.execute(
                link_table.update()
                    .where(link_table.c.id == target.id)
                    .values(schema_perm=target.get_schema_perm())
            )

        pvm_names = []
        if target.__tablename__ in {"dbs", "clusters"}:
            pvm_names.append(("database_access", target.get_perm()))
        else:
            pvm_names.append(("datasource_access", target.get_perm()))
            if target.schema:
                pvm_names.append(("schema_access", target.get_schema_perm()))

        for permission_name, view_menu_name in pvm_names:
            permission = self.find_permission(permission_name)
            view_menu = self.find_view_menu(view_menu_name)
            pv = None

            if not permission:
                permission_table = (
                    self.permission_model.__table__  # pylint: disable=no-member
                )
                connection.execute(
                    permission_table.insert().values(name=permission_name)
                )
                permission = self.find_permission(permission_name)
            if not view_menu:
                view_menu_table = (
                    self.viewmenu_model.__table__  # pylint: disable=no-member
                )
                connection.execute(view_menu_table.insert().values(name=view_menu_name))
                view_menu = self.find_view_menu(view_menu_name)

            if permission and view_menu:
                pv = (
                    self.get_session.query(self.permissionview_model)
                        .filter_by(permission=permission, view_menu=view_menu)
                        .first()
                )
            if not pv and permission and view_menu:
                permission_view_table = (
                    self.permissionview_model.__table__  # pylint: disable=no-member
                )
                connection.execute(
                    permission_view_table.insert().values(
                        permission_id=permission.id, view_menu_id=view_menu.id
                    )
                )

    def raise_for_access(
        self,
        database: Optional["Database"] = None,
        datasource: Optional["BaseDatasource"] = None,
        query: Optional["Query"] = None,
        query_context: Optional["QueryContext"] = None,
        table: Optional["Table"] = None,
        viz: Optional["BaseViz"] = None,
    ) -> None:
        """
        如果用户不能访问资源则引发异常。

        :param database: RabbitAI 数据库对象。
        :param datasource: RabbitAI 数据源对象。
        :param query: SQL 查询对象。
        :param query_context: 查询上下文。
        :param table: Rabbitai 数据表对象(要求数据库对象)
        :param viz: 可视对象。

        :raises RabbitaiSecurityException: 如果用户不能访问资源。
        """

        from rabbitai.connectors.sqla.models import SqlaTable
        from rabbitai.sql_parse import Table

        if database and table or query:
            if query:
                database = query.database

            database = cast("Database", database)

            if self.can_access_database(database):
                return

            if query:
                tables = {
                    Table(table_.table, table_.schema or query.schema)
                    for table_ in sql_parse.ParsedQuery(query.sql).tables
                }
            elif table:
                tables = {table}

            denied = set()

            for table_ in tables:
                schema_perm = self.get_schema_perm(database, schema=table_.schema)

                if not (schema_perm and self.can_access("schema_access", schema_perm)):
                    datasources = SqlaTable.query_datasources_by_name(
                        self.get_session, database, table_.table, schema=table_.schema
                    )

                    # Access to any datasource is suffice.
                    for datasource_ in datasources:
                        if self.can_access("datasource_access", datasource_.perm):
                            break
                    else:
                        denied.add(table_)

            if denied:
                raise RabbitaiSecurityException(
                    self.get_table_access_error_object(denied)
                )

        if datasource or query_context or viz:
            if query_context:
                datasource = query_context.datasource
            elif viz:
                datasource = viz.datasource

            assert datasource

            from rabbitai.extensions import feature_flag_manager

            if not (
                self.can_access_schema(datasource)
                or self.can_access("datasource_access", datasource.perm or "")
                or (
                    feature_flag_manager.is_feature_enabled("DASHBOARD_RBAC")
                    and self.can_access_based_on_dashboard(datasource)
                )
            ):
                raise RabbitaiSecurityException(
                    self.get_datasource_access_error_object(datasource)
                )

    def get_user_by_username(
        self, username: str, session: Session = None
    ) -> Optional[User]:
        """
        Retrieves a user by it's username case sensitive. Optional session parameter
        utility method normally useful for celery tasks where the session
        need to be scoped
        """
        session = session or self.get_session
        return (
            session.query(self.user_model)
                .filter(self.user_model.username == username)
                .one_or_none()
        )

    def get_anonymous_user(self) -> User:  # pylint: disable=no-self-use
        return AnonymousUserMixin()

    def get_rls_filters(self, table: "BaseDatasource") -> List[SqlaQuery]:
        """
        Retrieves the appropriate row level security filters for the current user and
        the passed table.

        :param table: The table to check against
        :returns: A list of filters
        """
        if hasattr(g, "user") and hasattr(g.user, "id"):
            from rabbitai.connectors.sqla.models import (
                RLSFilterRoles,
                RLSFilterTables,
                RowLevelSecurityFilter,
            )

            user_roles = (
                self.get_session.query(assoc_user_role.c.role_id)
                    .filter(assoc_user_role.c.user_id == g.user.get_id())
                    .subquery()
            )
            regular_filter_roles = (
                self.get_session.query(RLSFilterRoles.c.rls_filter_id)
                    .join(RowLevelSecurityFilter)
                    .filter(
                    RowLevelSecurityFilter.filter_type
                    == RowLevelSecurityFilterType.REGULAR
                )
                    .filter(RLSFilterRoles.c.role_id.in_(user_roles))
                    .subquery()
            )
            base_filter_roles = (
                self.get_session.query(RLSFilterRoles.c.rls_filter_id)
                    .join(RowLevelSecurityFilter)
                    .filter(
                    RowLevelSecurityFilter.filter_type
                    == RowLevelSecurityFilterType.BASE
                )
                    .filter(RLSFilterRoles.c.role_id.in_(user_roles))
                    .subquery()
            )
            filter_tables = (
                self.get_session.query(RLSFilterTables.c.rls_filter_id)
                    .filter(RLSFilterTables.c.table_id == table.id)
                    .subquery()
            )
            query = (
                self.get_session.query(
                    RowLevelSecurityFilter.id,
                    RowLevelSecurityFilter.group_key,
                    RowLevelSecurityFilter.clause,
                )
                    .filter(RowLevelSecurityFilter.id.in_(filter_tables))
                    .filter(
                    or_(
                        and_(
                            RowLevelSecurityFilter.filter_type
                            == RowLevelSecurityFilterType.REGULAR,
                            RowLevelSecurityFilter.id.in_(regular_filter_roles),
                        ),
                        and_(
                            RowLevelSecurityFilter.filter_type
                            == RowLevelSecurityFilterType.BASE,
                            RowLevelSecurityFilter.id.notin_(base_filter_roles),
                        ),
                    )
                )
            )
            return query.all()
        return []

    def get_rls_ids(self, table: "BaseDatasource") -> List[int]:
        """
        Retrieves the appropriate row level security filters IDs for the current user
        and the passed table.

        :param table: The table to check against
        :returns: A list of IDs
        """
        ids = [f.id for f in self.get_rls_filters(table)]
        ids.sort()  # Combinations rather than permutations
        return ids

    @staticmethod
    def raise_for_dashboard_access(dashboard: "Dashboard") -> None:
        """
        Raise an exception if the user cannot access the dashboard.

        :param dashboard: Dashboard the user wants access to
        :raises DashboardAccessDeniedError: If the user cannot access the resource
        """
        from rabbitai.dashboards.commands.exceptions import DashboardAccessDeniedError
        from rabbitai.views.base import get_user_roles, is_user_admin
        from rabbitai.views.utils import is_owner
        from rabbitai import is_feature_enabled

        if is_feature_enabled("DASHBOARD_RBAC"):
            has_rbac_access = any(
                dashboard_role.id in [user_role.id for user_role in get_user_roles()]
                for dashboard_role in dashboard.roles
            )
            can_access = (
                is_user_admin()
                or is_owner(dashboard, g.user)
                or (dashboard.published and has_rbac_access)
            )

            if not can_access:
                raise DashboardAccessDeniedError()

    @staticmethod
    def can_access_based_on_dashboard(datasource: "BaseDatasource") -> bool:
        """
        能否在仪表盘中访问指定数据源。

        :param datasource: 数据源对象。
        :return:
        """

        from rabbitai import db
        from rabbitai.dashboards.filters import DashboardAccessFilter
        from rabbitai.models.slice import Slice
        from rabbitai.models.dashboard import Dashboard

        datasource_class = type(datasource)
        query = (
            db.session.query(datasource_class)
                .join(Slice.table)
                .filter(datasource_class.id == datasource.id)
        )

        query = DashboardAccessFilter("id", SQLAInterface(Dashboard, db.session)).apply(
            query, None
        )

        exists = db.session.query(query.exists()).scalar()
        return exists
