# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, Text

from rabbitai.models.helpers import AuditMixinNullable


class DynamicPlugin(Model, AuditMixinNullable):
    """动态插件对象关系模型，定义列：id、name、key、bundle_url。"""

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    """插件名称"""
    key = Column(Text, unique=True, nullable=False)
    """键，对应静态插件的 viz_type"""
    bundle_url = Column(Text, unique=True, nullable=False)
    """插件资源打包地址。"""
    def __repr__(self) -> str:
        return str(self.name)
