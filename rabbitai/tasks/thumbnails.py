"""Utility functions used across Rabbitai"""

import logging
from typing import Optional

from flask import current_app

from rabbitai import app, security_manager, thumbnail_cache
from rabbitai.extensions import celery_app
from rabbitai.utils.celery import session_scope
from rabbitai.utils.screenshots import ChartScreenshot, DashboardScreenshot
from rabbitai.utils.webdriver import WindowSize

logger = logging.getLogger(__name__)


@celery_app.task(name="cache_chart_thumbnail", soft_time_limit=300)
def cache_chart_thumbnail(
    url: str,
    digest: str,
    force: bool = False,
    window_size: Optional[WindowSize] = None,
    thumb_size: Optional[WindowSize] = None,
) -> None:
    with app.app_context():  # type: ignore
        if not thumbnail_cache:
            logger.warning("No cache set, refusing to compute")
            return None
        logger.info("Caching chart: %s", url)
        screenshot = ChartScreenshot(url, digest)
        with session_scope(nullpool=True) as session:
            user = security_manager.get_user_by_username(
                current_app.config["THUMBNAIL_SELENIUM_USER"], session=session
            )
            screenshot.compute_and_cache(
                user=user,
                cache=thumbnail_cache,
                force=force,
                window_size=window_size,
                thumb_size=thumb_size,
            )
        return None


@celery_app.task(name="cache_dashboard_thumbnail", soft_time_limit=300)
def cache_dashboard_thumbnail(
    url: str, digest: str, force: bool = False, thumb_size: Optional[WindowSize] = None
) -> None:
    with app.app_context():  # type: ignore
        if not thumbnail_cache:
            logging.warning("No cache set, refusing to compute")
            return
        logger.info("Caching dashboard: %s", url)
        screenshot = DashboardScreenshot(url, digest)
        with session_scope(nullpool=True) as session:
            user = security_manager.get_user_by_username(
                current_app.config["THUMBNAIL_SELENIUM_USER"], session=session
            )
            screenshot.compute_and_cache(
                user=user, cache=thumbnail_cache, force=force, thumb_size=thumb_size,
            )
