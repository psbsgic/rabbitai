from typing import Any

from flask_babel import lazy_gettext as _
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from rabbitai.models.annotations import AnnotationLayer
from rabbitai.views.base import BaseFilter


class AnnotationLayerAllTextFilter(BaseFilter):
    """注释层文本过滤器。"""

    name = _("All Text")
    arg_name = "annotation_layer_all_text"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
            or_(
                AnnotationLayer.name.ilike(ilike_value),
                AnnotationLayer.descr.ilike(ilike_value),
            )
        )
