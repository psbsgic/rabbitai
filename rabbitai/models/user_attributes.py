# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from rabbitai import security_manager
from rabbitai.models.helpers import AuditMixinNullable


class UserAttribute(Model, AuditMixinNullable):
    """
    用户特性对象关系模型，附加到用户的自定义属性。

    扩展用户属性很棘手，因为它依赖于身份验证类型——RabbitAI 中的循环依赖。
    相反，我们使用自定义模型来添加属性。

    """

    __tablename__ = "user_attribute"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship(
        security_manager.user_model, backref="extra_attributes", foreign_keys=[user_id]
    )

    welcome_dashboard_id = Column(Integer, ForeignKey("dashboards.id"))
    welcome_dashboard = relationship("Dashboard")
