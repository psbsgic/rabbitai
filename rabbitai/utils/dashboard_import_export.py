# -*- coding: utf-8 -*-

import logging

from sqlalchemy.orm import Session

from rabbitai.models.dashboard import Dashboard

logger = logging.getLogger(__name__)


def export_dashboards(session: Session) -> str:
    """Returns all dashboards metadata as a json dump"""
    logger.info("Starting export")
    dashboards = session.query(Dashboard)
    dashboard_ids = []
    for dashboard in dashboards:
        dashboard_ids.append(dashboard.id)
    data = Dashboard.export_dashboards(dashboard_ids)
    return data
