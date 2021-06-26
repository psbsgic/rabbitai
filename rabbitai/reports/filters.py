from typing import Any

from flask_babel import lazy_gettext as _
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from rabbitai.models.reports import ReportSchedule
from rabbitai.views.base import BaseFilter


class ReportScheduleAllTextFilter(BaseFilter):  # pylint: disable=too-few-public-methods
    name = _("All Text")
    arg_name = "report_all_text"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
            or_(
                ReportSchedule.name.ilike(ilike_value),
                ReportSchedule.description.ilike(ilike_value),
                ReportSchedule.sql.ilike((ilike_value)),
            )
        )
