# -*- coding: utf-8 -*-

from typing import Any, Dict

from flask_appbuilder import Model
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from rabbitai.models.helpers import AuditMixinNullable


class AnnotationLayer(Model, AuditMixinNullable):
    """注释层对象关系模型，一组注释的逻辑命名空间"""

    __tablename__ = "annotation_layer"
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    descr = Column(Text)

    def __repr__(self) -> str:
        return str(self.name)


class Annotation(Model, AuditMixinNullable):
    """注释对象关系模型。"""

    __tablename__ = "annotation"

    id = Column(Integer, primary_key=True)
    start_dttm = Column(DateTime)
    end_dttm = Column(DateTime)
    layer_id = Column(Integer, ForeignKey("annotation_layer.id"), nullable=False)
    short_descr = Column(String(500))
    long_descr = Column(Text)
    layer = relationship(AnnotationLayer, backref="annotation")
    json_metadata = Column(Text)

    __table_args__ = (Index("ti_dag_state", layer_id, start_dttm, end_dttm),)

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "start_dttm": self.start_dttm,
            "end_dttm": self.end_dttm,
            "short_descr": self.short_descr,
            "long_descr": self.long_descr,
            "layer": self.layer.name if self.layer else None,
        }

    def __repr__(self) -> str:
        return str(self.short_descr)
