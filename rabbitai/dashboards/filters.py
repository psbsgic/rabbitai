# pylint: disable=too-few-public-methods
from typing import Any, Optional

from flask_appbuilder.security.sqla.models import Role
from flask_babel import lazy_gettext as _
from sqlalchemy import and_, or_
from sqlalchemy.orm.query import Query

from rabbitai import db, is_feature_enabled, security_manager
from rabbitai.models.core import FavStar
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice
from rabbitai.views.base import BaseFilter, get_user_roles, is_user_admin
from rabbitai.views.base_api import BaseFavoriteFilter


class DashboardTitleOrSlugFilter(BaseFilter):
    """仪表盘标题或类别过滤器。"""

    name = _("Title or Slug")
    arg_name = "title_or_slug"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
            or_(
                Dashboard.dashboard_title.ilike(ilike_value),
                Dashboard.slug.ilike(ilike_value),
            )
        )


class DashboardFavoriteFilter(BaseFavoriteFilter):
    """
    GET 列表的自定义筛选器，用于过滤用户收藏的所有仪表板。
    """

    arg_name = "dashboard_is_favorite"
    class_name = "Dashboard"
    model = Dashboard


class DashboardAccessFilter(BaseFilter):
    """
    仪表盘访问过滤器。

    依据以下条件列出仪表盘：
        1. 用户拥有的
        2. 用户收藏的
        3. 公开发布的(如果他们有至少一个切片访问权限)

    如果用户是管理员则显示所有仪表盘。
    这意味着他们没有获得策展权，但如果他们希望看到最先发布的仪表盘，仍然可以按 "published" 排序。
    """

    def apply(self, query: Query, value: Any) -> Query:
        if is_user_admin():
            return query

        datasource_perms = security_manager.user_view_menu_names("datasource_access")
        schema_perms = security_manager.user_view_menu_names("schema_access")

        is_rbac_disabled_filter = []
        dashboard_has_roles = Dashboard.roles.any()
        if is_feature_enabled("DASHBOARD_RBAC"):
            is_rbac_disabled_filter.append(~dashboard_has_roles)

        datasource_perm_query = (
            db.session.query(Dashboard.id)
            .join(Dashboard.slices)
            .filter(
                and_(
                    Dashboard.published.is_(True),
                    *is_rbac_disabled_filter,
                    or_(
                        Slice.perm.in_(datasource_perms),
                        Slice.schema_perm.in_(schema_perms),
                        security_manager.can_access_all_datasources(),
                    ),
                )
            )
        )

        users_favorite_dash_query = db.session.query(FavStar.obj_id).filter(
            and_(
                FavStar.user_id == security_manager.user_model.get_user_id(),
                FavStar.class_name == "Dashboard",
            )
        )
        owner_ids_query = (
            db.session.query(Dashboard.id)
            .join(Dashboard.owners)
            .filter(
                security_manager.user_model.id
                == security_manager.user_model.get_user_id()
            )
        )

        dashboard_rbac_or_filters = []
        if is_feature_enabled("DASHBOARD_RBAC"):
            roles_based_query = (
                db.session.query(Dashboard.id)
                .join(Dashboard.roles)
                .filter(
                    and_(
                        Dashboard.published.is_(True),
                        dashboard_has_roles,
                        Role.id.in_([x.id for x in get_user_roles()]),
                    ),
                )
            )

            dashboard_rbac_or_filters.append(Dashboard.id.in_(roles_based_query))

        query = query.filter(
            or_(
                Dashboard.id.in_(owner_ids_query),
                Dashboard.id.in_(datasource_perm_query),
                Dashboard.id.in_(users_favorite_dash_query),
                *dashboard_rbac_or_filters,
            )
        )

        return query


class FilterRelatedRoles(BaseFilter):
    """
    允许搜索资源的关联角色的过滤器。

    通过添加以下内容在api中使用：
    related_field_filters = {
      "roles": RelatedFieldFilter("name", FilterRelatedRoles),
    }
    """

    name = _("Role")
    arg_name = "roles"

    def apply(self, query: Query, value: Optional[Any]) -> Query:
        role_model = security_manager.role_model
        if value:
            return query.filter(role_model.name.ilike(f"%{value}%"),)
        return query
