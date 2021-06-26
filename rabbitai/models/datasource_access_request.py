from typing import Optional, Type, TYPE_CHECKING

from flask import Markup
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

from rabbitai import app, db, security_manager
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.models.helpers import AuditMixinNullable
from rabbitai.utils import core as utils

if TYPE_CHECKING:
    from rabbitai.connectors.base.models import BaseDatasource

config = app.config


class DatasourceAccessRequest(Model, AuditMixinNullable):
    """访问数据源和数据库请求 ORM。"""

    __tablename__ = "access_request"
    id = Column(Integer, primary_key=True)

    datasource_id = Column(Integer)
    datasource_type = Column(String(200))

    ROLES_DENYLIST = set(config["ROBOT_PERMISSION_ROLES"])

    @property
    def cls_model(self) -> Type["BaseDatasource"]:
        return ConnectorRegistry.sources[self.datasource_type]

    @property
    def username(self) -> Markup:
        return self.creator()

    @property
    def datasource(self) -> "BaseDatasource":
        return self.get_datasource

    @datasource.getter  # type: ignore
    @utils.memoized
    def get_datasource(self) -> "BaseDatasource":
        ds = db.session.query(self.cls_model).filter_by(id=self.datasource_id).first()
        return ds

    @property
    def datasource_link(self) -> Optional[Markup]:
        return self.datasource.link  # pylint: disable=no-member

    @property
    def roles_with_datasource(self) -> str:
        action_list = ""
        perm = self.datasource.perm  # pylint: disable=no-member
        pv = security_manager.find_permission_view_menu("datasource_access", perm)
        for role in pv.role:
            if role.name in self.ROLES_DENYLIST:
                continue
            href = (
                f"/rabbitai/approve?datasource_type={self.datasource_type}&"
                f"datasource_id={self.datasource_id}&"
                f"created_by={self.created_by.username}&role_to_grant={role.name}"
            )
            link = '<a href="{}">Grant {} Role</a>'.format(href, role.name)
            action_list = action_list + "<li>" + link + "</li>"
        return "<ul>" + action_list + "</ul>"

    @property
    def user_roles(self) -> str:
        action_list = ""
        for role in self.created_by.roles:
            href = (
                f"/rabbitai/approve?datasource_type={self.datasource_type}&"
                f"datasource_id={self.datasource_id}&"
                f"created_by={self.created_by.username}&role_to_extend={role.name}"
            )
            link = '<a href="{}">Extend {} Role</a>'.format(href, role.name)
            if role.name in self.ROLES_DENYLIST:
                link = "{} Role".format(role.name)
            action_list = action_list + "<li>" + link + "</li>"
        return "<ul>" + action_list + "</ul>"
