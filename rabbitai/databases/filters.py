from typing import Any, Set

from sqlalchemy import or_
from sqlalchemy.orm import Query

from rabbitai import security_manager
from rabbitai.views.base import BaseFilter


class DatabaseFilter(BaseFilter):
    """数据库过滤器。"""

    def schema_access_databases(self) -> Set[str]:
        """模式访问数据库。"""

        return {
            security_manager.unpack_schema_perm(vm)[0]
            for vm in security_manager.user_view_menu_names("schema_access")
        }

    def apply(self, query: Query, value: Any) -> Query:
        """
        应用该过滤到指定查询。

        :param query: 查询对象。
        :param value: 值。
        :return:
        """

        if security_manager.can_access_all_databases():
            return query

        database_perms = security_manager.user_view_menu_names("database_access")

        schema_access_databases = self.schema_access_databases()

        return query.filter(
            or_(
                self.model.perm.in_(database_perms),
                self.model.database_name.in_(schema_access_databases),
            )
        )
