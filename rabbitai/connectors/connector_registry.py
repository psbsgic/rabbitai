from typing import Dict, List, Optional, Set, Type, TYPE_CHECKING

from sqlalchemy import or_
from sqlalchemy.orm import Session, subqueryload

from rabbitai.datasets.commands.exceptions import DatasetNotFoundError

if TYPE_CHECKING:
    from collections import OrderedDict

    from rabbitai.connectors.base.models import BaseDatasource
    from rabbitai.models.core import Database


class ConnectorRegistry:
    """ 所有可用数据源引擎注册表，统一集中注册和管理应用程序要使用的数据源。"""

    sources: Dict[str, Type["BaseDatasource"]] = {}
    """已注册的数据源字典（数据源类型和实例）"""

    @classmethod
    def register_sources(cls, datasource_config: "OrderedDict[str, List[str]]") -> None:
        """
        注册指定数据源配置对象提供的数据源，加载定义数据源类的模块，实例化数据源类实例并缓存。

        :param datasource_config: 数据源配置对象，一个模块名称和类名称列表的有序字典。
        :return:
        """

        for module_name, class_names in datasource_config.items():
            class_names = [str(s) for s in class_names]
            module_obj = __import__(module_name, fromlist=class_names)
            for class_name in class_names:
                source_class = getattr(module_obj, class_name)
                cls.sources[source_class.type] = source_class

    @classmethod
    def get_datasource(
        cls, datasource_type: str, datasource_id: int, session: Session
    ) -> "BaseDatasource":
        """
        依据指定数据源类型和标识，获取数据源对象实例，如果不存在则引发异常 `DatasetNotFoundError` 。

        :param datasource_type: 数据源类型。
        :param datasource_id: 数据源标识。
        :param session: 数据库会话对象。
        :return:
        """

        if datasource_type not in cls.sources:
            raise DatasetNotFoundError()

        # 从数据库中查询数据源
        datasource = (
            session.query(cls.sources[datasource_type])
            .filter_by(id=datasource_id)
            .one_or_none()
        )

        if not datasource:
            raise DatasetNotFoundError()

        return datasource

    @classmethod
    def get_all_datasources(cls, session: Session) -> List["BaseDatasource"]:
        """
        返回所有数据源对象的列表。

        :param session: 数据库会话对象。
        :return: 数据源对象的列表。
        """

        datasources: List["BaseDatasource"] = []
        for source_type in ConnectorRegistry.sources:
            source_class = ConnectorRegistry.sources[source_type]
            qry = session.query(source_class)
            qry = source_class.default_query(qry)
            datasources.extend(qry.all())

        return datasources

    @classmethod
    def get_datasource_by_name(
        cls,
        session: Session,
        datasource_type: str,
        datasource_name: str,
        schema: str,
        database_name: str,
    ) -> Optional["BaseDatasource"]:
        """
        返回具有指定名称的数据源对象。

        :param session: 数据库会话对象。
        :param datasource_type: 数据源类型。
        :param datasource_name: 数据源名称。
        :param schema: 模式。
        :param database_name: 数据库名称。
        :return:
        """

        datasource_class = ConnectorRegistry.sources[datasource_type]
        return datasource_class.get_datasource_by_name(
            session, datasource_name, schema, database_name
        )

    @classmethod
    def query_datasources_by_permissions(
        cls,
        session: Session,
        database: "Database",
        permissions: Set[str],
        schema_perms: Set[str],
    ) -> List["BaseDatasource"]:
        """
        按照权限查询数据源。

        :param session: 数据库会话对象。
        :param database: 数据库对象。
        :param permissions: 权限。
        :param schema_perms: 模式权限。
        :return:
        """

        datasource_class = ConnectorRegistry.sources[database.type]
        return (
            session.query(datasource_class)
            .filter_by(database_id=database.id)
            .filter(
                or_(
                    datasource_class.perm.in_(permissions),
                    datasource_class.schema_perm.in_(schema_perms),
                )
            )
            .all()
        )

    @classmethod
    def get_eager_datasource(
        cls, session: Session, datasource_type: str, datasource_id: int
    ) -> "BaseDatasource":
        """
        返回具有列和指标的数据源对象。

        :param session:
        :param datasource_type:
        :param datasource_id:
        :return:
        """

        datasource_class = ConnectorRegistry.sources[datasource_type]
        return (
            session.query(datasource_class)
            .options(
                subqueryload(datasource_class.columns),
                subqueryload(datasource_class.metrics),
            )
            .filter_by(id=datasource_id)
            .one()
        )

    @classmethod
    def query_datasources_by_name(
        cls,
        session: Session,
        database: "Database",
        datasource_name: str,
        schema: Optional[str] = None,
    ) -> List["BaseDatasource"]:
        """
        按照名称查询数据源对象。

        :param session:
        :param database:
        :param datasource_name:
        :param schema:
        :return:
        """
        datasource_class = ConnectorRegistry.sources[database.type]
        return datasource_class.query_datasources_by_name(
            session, database, datasource_name, schema=schema
        )
