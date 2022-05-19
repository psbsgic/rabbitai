from flask_babel import lazy_gettext as _
from sqlalchemy import not_, or_
from sqlalchemy.orm.query import Query

from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.views.base import BaseFilter


class DatasetIsNullOrEmptyFilter(BaseFilter):
    """数据集是否为Null或空过滤器。"""

    name = _("Null or Empty")
    arg_name = "dataset_is_null_or_empty"

    def apply(self, query: Query, value: bool) -> Query:
        filter_clause = or_(SqlaTable.sql.is_(None), SqlaTable.sql == "")

        if not value:
            filter_clause = not_(filter_clause)

        return query.filter(filter_clause)
