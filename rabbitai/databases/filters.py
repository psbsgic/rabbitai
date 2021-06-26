from typing import Any, Set

from sqlalchemy import or_
from sqlalchemy.orm import Query

from rabbitai import security_manager
from rabbitai.views.base import BaseFilter


class DatabaseFilter(BaseFilter):
    # TODO(bogdan): consider caching.
    def schema_access_databases(self) -> Set[str]:  # noqa pylint: disable=no-self-use
        return {
            security_manager.unpack_schema_perm(vm)[0]
            for vm in security_manager.user_view_menu_names("schema_access")
        }

    def apply(self, query: Query, value: Any) -> Query:
        if security_manager.can_access_all_databases():
            return query
        database_perms = security_manager.user_view_menu_names("database_access")
        # TODO(bogdan): consider adding datasource access here as well.
        schema_access_databases = self.schema_access_databases()
        return query.filter(
            or_(
                self.model.perm.in_(database_perms),
                self.model.database_name.in_(schema_access_databases),
            )
        )
