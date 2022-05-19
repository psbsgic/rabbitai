# -*- coding: utf-8 -*-

from typing import Optional, Type, TYPE_CHECKING

from flask import Markup
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

from rabbitai import app, db, security_manager
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.models.helpers import AuditMixinNullable
from rabbitai.utils.memoized import memoized

if TYPE_CHECKING:
    from rabbitai.connectors.base.models import BaseDatasource

config = app.config


class DatasourceAccessRequest(Model, AuditMixinNullable):
    """数据源和数据库访问请求的 ORM 模型，存储：id、datasource_id和datasource_type（数据源标识和类型）。"""

    __tablename__ = "access_request"

    id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer)
    datasource_type = Column(String(200))

    ROLES_DENYLIST = set(config["ROBOT_PERMISSION_ROLES"])
    """拒绝访问的角色集合"""

    @property
    def cls_model(self) -> Type["BaseDatasource"]:
        """获取数据源的对象关系模型类。"""
        return ConnectorRegistry.sources[self.datasource_type]

    @property
    def username(self) -> Markup:
        """获取用户名称，即创建者。"""
        return self.creator()

    @property
    def datasource(self) -> "BaseDatasource":
        """获取数据源对象。"""
        return self.get_datasource

    @datasource.getter
    @memoized
    def get_datasource(self) -> "BaseDatasource":
        """从数据库中获取数据源对象并缓存。"""
        ds = db.session.query(self.cls_model).filter_by(id=self.datasource_id).first()
        return ds

    @property
    def datasource_link(self) -> Optional[Markup]:
        """获取数据源访问连接。"""
        return self.datasource.link

    @property
    def roles_with_datasource(self) -> str:
        """
        获取角色和数据源的Html列表 ul。

        :return:
        """

        action_list = ""
        perm = self.datasource.perm
        pv = security_manager.find_permission_view_menu("datasource_access", perm)
        for role in pv.role:
            if role.name in self.ROLES_DENYLIST:
                continue

            href = (
                f"/rabbitai/approve?datasource_type={self.datasource_type}&"
                f"datasource_id={self.datasource_id}&"
                f"created_by={self.created_by.username}&role_to_grant={role.name}"
            )
            link = '<a href="{}">授权 {} 角色</a>'.format(href, role.name)
            action_list = action_list + "<li>" + link + "</li>"
        return "<ul>" + action_list + "</ul>"

    @property
    def user_roles(self) -> str:
        """返回用户角色ul元素。"""

        action_list = ""
        for role in self.created_by.roles:
            href = (
                f"/rabbitai/approve?datasource_type={self.datasource_type}&"
                f"datasource_id={self.datasource_id}&"
                f"created_by={self.created_by.username}&role_to_extend={role.name}"
            )
            link = '<a href="{}">扩展 {} 角色</a>'.format(href, role.name)
            if role.name in self.ROLES_DENYLIST:
                link = "{} 角色".format(role.name)
            action_list = action_list + "<li>" + link + "</li>"
        return "<ul>" + action_list + "</ul>"
