# -*- coding: utf-8 -*-

import logging

from sqlalchemy.orm import Session

from rabbitai.models.dashboard import Dashboard

logger = logging.getLogger(__name__)


def export_dashboards(session: Session) -> str:
    """
    返回所有仪表盘元数据为 Json 格式字符串。

    :param session: 数据库会话对象。
    :type session: Session
    :return: Json格式字符串。
    :rtype: str
    """

    logger.info("Starting export")
    dashboards = session.query(Dashboard)
    dashboard_ids = []
    for dashboard in dashboards:
        dashboard_ids.append(dashboard.id)
    data = Dashboard.export_dashboards(dashboard_ids)

    return data
