# -*- coding: utf-8 -*-

from typing import Any

from flask import g
from flask_sqlalchemy import BaseQuery

from rabbitai import security_manager
from rabbitai.models.sql_lab import Query
from rabbitai.views.base import BaseFilter


class QueryFilter(BaseFilter):
    def apply(self, query: BaseQuery, value: Any) -> BaseQuery:
        """
        Filter queries to only those owned by current user. If
        can_access_all_queries permission is set a user can list all queries

        :returns: query
        """
        if not security_manager.can_access_all_queries():
            query = query.filter(Query.user_id == g.user.get_user_id())
        return query
