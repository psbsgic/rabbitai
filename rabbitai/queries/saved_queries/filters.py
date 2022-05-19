# -*- coding: utf-8 -*-

from typing import Any

from flask import g
from flask_babel import lazy_gettext as _
from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from rabbitai.models.sql_lab import SavedQuery
from rabbitai.views.base import BaseFilter
from rabbitai.views.base_api import BaseFavoriteFilter


class SavedQueryAllTextFilter(BaseFilter):
    """保存的查询全文检索过滤器。"""

    name = _("All Text")
    arg_name = "all_text"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
            or_(
                SavedQuery.schema.ilike(ilike_value),
                SavedQuery.label.ilike(ilike_value),
                SavedQuery.description.ilike(ilike_value),
                SavedQuery.sql.ilike(ilike_value),
            )
        )


class SavedQueryFavoriteFilter(BaseFavoriteFilter):
    """
    返回用户关注的保存的查询过滤器。
    """

    arg_name = "saved_query_is_fav"
    class_name = "query"
    model = SavedQuery


class SavedQueryFilter(BaseFilter):
    """保存的查询过滤器，返回当前用户创建的查询对象。"""

    def apply(self, query: BaseQuery, value: Any) -> BaseQuery:
        """
        Filter saved queries to only those created by current user.

        :returns: flask-sqlalchemy query
        """
        return query.filter(SavedQuery.created_by == g.user)
