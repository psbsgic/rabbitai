# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Set, Type, TYPE_CHECKING

from flask_babel import _
from sqlalchemy import or_
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy.orm.exc import NoResultFound

from rabbitai.datasets.commands.exceptions import DatasetNotFoundError

if TYPE_CHECKING:
    from collections import OrderedDict

    from rabbitai.connectors.base.models import BaseDatasource
    from rabbitai.models.core import Database


class ConnectorRegistry:
    """
    所有可用数据源引擎的注册表，通过 register_sources 方法注册可用数据源。
    使用数据源类型和数据源对象关系模型 `BaseDatasource` 实例的字典 sources 存储数据源，提供依据数据源类型从数据库访问数据源对象实例的方法。
    """

    sources: Dict[str, Type["BaseDatasource"]] = {}
    """数据源类型和数据源对象关系模型 BaseDatasource 实例的字典。"""

    @classmethod
    def register_sources(cls, datasource_config: "OrderedDict[str, List[str]]") -> None:
        """
        注册指定模块名称及其类名称列表的字典提供的数据源到该注册表，导入模块获取类实例。

        :param datasource_config: 模块名称和数据源类名称列表的字典。
        :return: None。
        """

        for module_name, class_names in datasource_config.items():
            class_names = [str(s) for s in class_names]
            module_obj = __import__(module_name, fromlist=class_names)
            for class_name in class_names:
                source_class = getattr(module_obj, class_name)
                cls.sources[source_class.type] = source_class

    # region 获取数据源

    @classmethod
    def get_datasource(cls, datasource_type: str, datasource_id: int, session: Session) -> "BaseDatasource":
        """
        依据指定数据源类型和数据源标识，安全的从数据库中获取数据源实例，即  `BaseDatasource` 的派生类型实例。

        如果 `datasource_type` 未注册或 `datasource_id` 不存在，则 raises `DatasetNotFoundError`。

        :param datasource_type: 数据源的类型。
        :param datasource_id: 数据源标识。
        :param session: 数据库会话对象。
        :return: 数据源实例。
        """

        if datasource_type not in cls.sources:
            raise DatasetNotFoundError()

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
        从数据库中获取所有数据源对象实例。

        :param session: 数据库会话对象。
        :return:
        """

        datasources: List["BaseDatasource"] = []
        for source_type in ConnectorRegistry.sources:
            source_class = ConnectorRegistry.sources[source_type]
            qry = session.query(source_class)
            qry = source_class.default_query(qry)
            datasources.extend(qry.all())
        return datasources

    @classmethod
    def get_datasource_by_id(cls, session: Session, datasource_id: int,) -> "BaseDatasource":
        """
        从数据库中查找具有指定标识的数据源对象实例。

        :param session: 数据库会话对象。
        :param datasource_id: 数据源标识。
        :return: 数据源对象实例。
        :raises NoResultFound: 如果未找到具有指定标识的数据源。
        """

        for datasource_class in ConnectorRegistry.sources.values():
            try:
                return (
                    session.query(datasource_class)
                    .filter(datasource_class.id == datasource_id)
                    .one()
                )
            except NoResultFound:
                # proceed to next datasource type
                pass
        raise NoResultFound(_("Datasource id not found: %(id)s", id=datasource_id))

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
        获取具有指定名称的数据源对象实例。

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
        :param database: 数据库对象实例。
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
        返回包含列和指标的数据源模型实例。

        :param session: 数据库会话对象。
        :param datasource_type: 数据源类型。
        :param datasource_id: 数据源标识。
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
        查找具有指定名称的数据源对象实例。

        :param session: 数据库会话对象。
        :param database: 数据库数据模型实例。
        :param datasource_name: 数据源名称。
        :param schema: 模式。
        :return: 数据源模型实例。
        """

        datasource_class = ConnectorRegistry.sources[database.type]
        return datasource_class.query_datasources_by_name(
            session, database, datasource_name, schema=schema
        )

    # endregion
