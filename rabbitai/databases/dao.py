import logging
from typing import Any, Dict, Optional

from rabbitai.dao.base import BaseDAO
from rabbitai.databases.filters import DatabaseFilter
from rabbitai.extensions import db
from rabbitai.models.core import Database
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice

logger = logging.getLogger(__name__)


class DatabaseDAO(BaseDAO):
    model_cls = Database
    base_filter = DatabaseFilter

    @staticmethod
    def validate_uniqueness(database_name: str) -> bool:
        database_query = db.session.query(Database).filter(
            Database.database_name == database_name
        )
        return not db.session.query(database_query.exists()).scalar()

    @staticmethod
    def validate_update_uniqueness(database_id: int, database_name: str) -> bool:
        database_query = db.session.query(Database).filter(
            Database.database_name == database_name, Database.id != database_id,
        )
        return not db.session.query(database_query.exists()).scalar()

    @staticmethod
    def get_database_by_name(database_name: str) -> Optional[Database]:
        return (
            db.session.query(Database)
            .filter(Database.database_name == database_name)
            .one_or_none()
        )

    @staticmethod
    def build_db_for_connection_test(
        server_cert: str, extra: str, impersonate_user: bool, encrypted_extra: str
    ) -> Database:
        return Database(
            server_cert=server_cert,
            extra=extra,
            impersonate_user=impersonate_user,
            encrypted_extra=encrypted_extra,
        )

    @classmethod
    def get_related_objects(cls, database_id: int) -> Dict[str, Any]:
        datasets = cls.find_by_id(database_id).tables
        dataset_ids = [dataset.id for dataset in datasets]

        charts = (
            db.session.query(Slice)
            .filter(
                Slice.datasource_id.in_(dataset_ids), Slice.datasource_type == "table"
            )
            .all()
        )
        chart_ids = [chart.id for chart in charts]

        dashboards = (
            (
                db.session.query(Dashboard)
                .join(Dashboard.slices)
                .filter(Slice.id.in_(chart_ids))
            )
            .distinct()
            .all()
        )
        return dict(charts=charts, dashboards=dashboards)
