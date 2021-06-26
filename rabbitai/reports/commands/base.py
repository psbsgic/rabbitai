import logging
from typing import Any, Dict, List

from marshmallow import ValidationError

from rabbitai.charts.dao import ChartDAO
from rabbitai.commands.base import BaseCommand
from rabbitai.dashboards.dao import DashboardDAO
from rabbitai.reports.commands.exceptions import (
    ChartNotFoundValidationError,
    DashboardNotFoundValidationError,
    ReportScheduleChartOrDashboardValidationError,
)

logger = logging.getLogger(__name__)


class BaseReportScheduleCommand(BaseCommand):

    _properties: Dict[str, Any]

    def run(self) -> Any:
        pass

    def validate(self) -> None:
        pass

    def validate_chart_dashboard(
        self, exceptions: List[ValidationError], update: bool = False
    ) -> None:
        """ Validate chart or dashboard relation """
        chart_id = self._properties.get("chart")
        dashboard_id = self._properties.get("dashboard")
        if chart_id and dashboard_id:
            exceptions.append(ReportScheduleChartOrDashboardValidationError())
        if chart_id:
            chart = ChartDAO.find_by_id(chart_id)
            if not chart:
                exceptions.append(ChartNotFoundValidationError())
            self._properties["chart"] = chart
        elif dashboard_id:
            dashboard = DashboardDAO.find_by_id(dashboard_id)
            if not dashboard:
                exceptions.append(DashboardNotFoundValidationError())
            self._properties["dashboard"] = dashboard
        elif not update:
            exceptions.append(ReportScheduleChartOrDashboardValidationError())
