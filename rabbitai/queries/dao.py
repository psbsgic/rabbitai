# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from rabbitai.dao.base import BaseDAO
from rabbitai.extensions import db
from rabbitai.models.sql_lab import Query, SavedQuery
from rabbitai.queries.filters import QueryFilter

logger = logging.getLogger(__name__)


class QueryDAO(BaseDAO):
    """对查询对象 Query 实现CRUD操作。"""

    model_cls = Query
    base_filter = QueryFilter

    @staticmethod
    def update_saved_query_exec_info(query_id: int) -> None:
        """
        Propagates query execution info back to saved query if applicable

        :param query_id: The query id
        :return:
        """
        query = db.session.query(Query).get(query_id)
        related_saved_queries = (
            db.session.query(SavedQuery)
            .filter(SavedQuery.database == query.database)
            .filter(SavedQuery.sql == query.sql)
        ).all()
        if related_saved_queries:
            for saved_query in related_saved_queries:
                saved_query.rows = query.rows
                saved_query.last_run = datetime.now()
            db.session.commit()
