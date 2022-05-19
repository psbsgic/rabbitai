# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.connectors.druid.models import DruidCluster
from rabbitai.models.core import Database

EXPORT_VERSION = "1.0.0"
DATABASES_KEY = "databases"
DRUID_CLUSTERS_KEY = "druid_clusters"
logger = logging.getLogger(__name__)


def export_schema_to_dict(back_references: bool) -> Dict[str, Any]:
    """Exports the supported import/export schema to a dictionary"""

    databases = [
        Database.export_schema(recursive=True, include_parent_ref=back_references)
    ]
    clusters = [
        DruidCluster.export_schema(recursive=True, include_parent_ref=back_references)
    ]
    data = dict()
    if databases:
        data[DATABASES_KEY] = databases
    if clusters:
        data[DRUID_CLUSTERS_KEY] = clusters
    return data


def export_to_dict(
    session: Session, recursive: bool, back_references: bool, include_defaults: bool
) -> Dict[str, Any]:
    """Exports databases and druid clusters to a dictionary"""

    logger.info("Starting export")
    dbs = session.query(Database)
    databases = [
        database.export_to_dict(
            recursive=recursive,
            include_parent_ref=back_references,
            include_defaults=include_defaults,
        )
        for database in dbs
    ]
    logger.info("Exported %d %s", len(databases), DATABASES_KEY)
    cls = session.query(DruidCluster)
    clusters = [
        cluster.export_to_dict(
            recursive=recursive,
            include_parent_ref=back_references,
            include_defaults=include_defaults,
        )
        for cluster in cls
    ]
    logger.info("Exported %d %s", len(clusters), DRUID_CLUSTERS_KEY)
    data = dict()
    if databases:
        data[DATABASES_KEY] = databases
    if clusters:
        data[DRUID_CLUSTERS_KEY] = clusters
    return data
