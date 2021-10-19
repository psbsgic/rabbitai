# -*- coding: utf-8 -*-

from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from rabbitai import security_manager
from rabbitai.views.base import BaseFilter


class SliceFilter(BaseFilter):
    def apply(self, query: Query, value: Any) -> Query:
        if security_manager.can_access_all_datasources():
            return query
        perms = security_manager.user_view_menu_names("datasource_access")
        schema_perms = security_manager.user_view_menu_names("schema_access")
        return query.filter(
            or_(self.model.perm.in_(perms), self.model.schema_perm.in_(schema_perms))
        )
