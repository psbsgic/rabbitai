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
    Helper function for commands, will fetch all users from owners id's
    Can raise ValidationError
    :param user: The current user
    :param owner_ids: A List of owners by id's
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
    Helper function for commands, will fetch all roles from roles id's
     :raises RolesNotFoundValidationError: If a role in the input list is not found
    :param role_ids: A List of roles by id's
    """
    roles: List[Role] = []
    if role_ids:
        roles = security_manager.find_roles_by_id(role_ids)
        if len(roles) != len(role_ids):
            raise RolesNotFoundValidationError()
    return roles


def get_datasource_by_id(datasource_id: int, datasource_type: str) -> BaseDatasource:
    try:
        return ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
    except DatasetNotFoundError:
        raise DatasourceNotFoundValidationError()
