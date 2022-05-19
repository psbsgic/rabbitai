from typing import List, Optional

from flask_appbuilder.security.sqla.models import Role, User

from rabbitai.commands.exceptions import (
    DatasourceNotFoundValidationError,
    OwnersNotFoundValidationError,
    RolesNotFoundValidationError,
)
from rabbitai.connectors.base.models import BaseDatasource
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.datasets.commands.exceptions import DatasetNotFoundError
from rabbitai.extensions import db, security_manager


def populate_owners(user: User, owner_ids: Optional[List[int]] = None) -> List[User]:
    """
    依据指定拥有者标识列表，返回所有相应的用户模型对象。

    可能引发异常 ValidationError

    :param user: 当前用户对象。
    :param owner_ids: 拥有者标识列表。
    """

    owners = list()
    if not owner_ids:
        return [user]
    if user.id not in owner_ids:
        owners.append(user)
    for owner_id in owner_ids:
        owner = security_manager.get_user_by_id(owner_id)
        if not owner:
            raise OwnersNotFoundValidationError()
        owners.append(owner)
    return owners


def populate_roles(role_ids: Optional[List[int]] = None) -> List[Role]:
    """
    返回指定角色标识列表对应的角色对象列表。
     :raises RolesNotFoundValidationError: 如果没有找到角色标识列表中对应的角色对象。
    :param role_ids: 角色标识列表。
    """

    roles: List[Role] = []
    if role_ids:
        roles = security_manager.find_roles_by_id(role_ids)
        if len(roles) != len(role_ids):
            raise RolesNotFoundValidationError()
    return roles


def get_datasource_by_id(datasource_id: int, datasource_type: str) -> BaseDatasource:
    """
    依据指定数据源标识和类型，从 ConnectorRegistry 返回数据源模型对象实例。

    :param datasource_id: 数据源标识。
    :param datasource_type: 数据源类型。
    :return: 数据源模型对象实例。
    """

    try:
        return ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
    except DatasetNotFoundError:
        raise DatasourceNotFoundValidationError()
