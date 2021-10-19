# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, Text

from rabbitai.models.helpers import AuditMixinNullable


class DynamicPlugin(Model, AuditMixinNullable):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    # key corresponds to viz_type from static plugins
    key = Column(Text, unique=True, nullable=False)
    bundle_url = Column(Text, unique=True, nullable=False)

    def __repr__(self) -> str:
        return str(self.name)
