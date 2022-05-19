# -*- coding: utf-8 -*-

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
    """数据库对象关系模型数据访问对象。"""

    model_cls = Database
    base_filter = DatabaseFilter

    @staticmethod
    def validate_uniqueness(database_name: str) -> bool:
        """
        验证唯一性。

        :param database_name: 数据库名称。
        :return:
        """

        database_query = db.session.query(Database).filter(
            Database.database_name == database_name
        )
        return not db.session.query(database_query.exists()).scalar()

    @staticmethod
    def validate_update_uniqueness(database_id: int, database_name: str) -> bool:
        """
        验证更新唯一性。

        :param database_id: 数据库标识。
        :param database_name: 数据库名称。
        :return:
        """

        database_query = db.session.query(Database).filter(
            Database.database_name == database_name, Database.id != database_id,
        )
        return not db.session.query(database_query.exists()).scalar()

    @staticmethod
    def get_database_by_name(database_name: str) -> Optional[Database]:
        """
        从数据库中返回具有指定数据库名称的数据库对象。

        :param database_name: 数据库名称。
        :return:
        """
        return (
            db.session.query(Database)
            .filter(Database.database_name == database_name)
            .one_or_none()
        )

    @staticmethod
    def build_db_for_connection_test(
        server_cert: str, extra: str, impersonate_user: bool, encrypted_extra: str
    ) -> Database:
        """
        构建连接测试数据库对象。

        :param server_cert: 服务器证书。
        :param extra: 额外数据。
        :param impersonate_user: 是否模拟用户。
        :param encrypted_extra: 加密额外数据。
        :return: 数据库对象。
        """

        return Database(
            server_cert=server_cert,
            extra=extra,
            impersonate_user=impersonate_user,
            encrypted_extra=encrypted_extra,
        )

    @classmethod
    def get_related_objects(cls, database_id: int) -> Dict[str, Any]:
        """
        获取与指定数据库对象相关的对象（图表、仪表盘等）列表。

        :param database_id: 数据库标识。
        :return:
        """

        # 数据表
        datasets = cls.find_by_id(database_id).tables
        dataset_ids = [dataset.id for dataset in datasets]

        # 图表
        charts = (
            db.session.query(Slice)
            .filter(
                Slice.datasource_id.in_(dataset_ids), Slice.datasource_type == "table"
            )
            .all()
        )
        chart_ids = [chart.id for chart in charts]

        # 仪表盘
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
