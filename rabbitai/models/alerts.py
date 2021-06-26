"""作业的计划执行相关模型"""

import json
import textwrap
from datetime import datetime
from typing import Any, Optional

from flask_appbuilder import Model
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship, RelationshipProperty

from rabbitai import db, security_manager
from rabbitai.models.helpers import AuditMixinNullable

metadata = Model.metadata


alert_owner = Table(
    "alert_owner",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("ab_user.id")),
    Column("alert_id", Integer, ForeignKey("alerts.id")),
)
"""更改提醒拥有者数据表"""


class Alert(Model, AuditMixinNullable):
    """更改提醒对象关系模型。"""

    __tablename__ = "alerts"

    # region 列定义

    id = Column(Integer, primary_key=True)
    label = Column(String(150), nullable=False)
    active = Column(Boolean, default=True, index=True)
    crontab = Column(String(50), nullable=False)

    alert_type = Column(String(50))
    owners = relationship(security_manager.user_model, secondary=alert_owner)
    recipients = Column(Text)
    slack_channel = Column(Text)

    log_retention = Column(Integer, default=90)
    grace_period = Column(Integer, default=60 * 60 * 24)

    slice_id = Column(Integer, ForeignKey("slices.id"))
    slice = relationship("Slice", backref="alerts", foreign_keys=[slice_id])

    dashboard_id = Column(Integer, ForeignKey("dashboards.id"))
    dashboard = relationship("Dashboard", backref="alert", foreign_keys=[dashboard_id])

    last_eval_dttm = Column(DateTime, default=datetime.utcnow)
    last_state = Column(String(10))

    # Observation related columns
    sql = Column(Text, nullable=False)

    # Validation related columns
    validator_type = Column(String(100), nullable=False)
    validator_config = Column(
        Text,
        default=textwrap.dedent(
            """
            {

            }
            """
        ),
    )

    @declared_attr
    def database_id(self) -> int:
        return Column(Integer, ForeignKey("dbs.id"), nullable=False)

    @declared_attr
    def database(self) -> RelationshipProperty:
        return relationship(
            "Database",
            foreign_keys=[self.database_id],
            backref=backref("sql_observers", cascade="all, delete-orphan"),
        )

    # endregion

    def get_last_observation(self) -> Optional[Any]:
        observations = list(
            db.session.query(SQLObservation)
            .filter_by(alert_id=self.id)
            .order_by(SQLObservation.dttm.desc())
            .limit(1)
        )

        if observations:
            return observations[0]

        return None

    def __str__(self) -> str:
        return f"<{self.id}:{self.label}>"

    @property
    def pretty_config(self) -> str:
        """ String representing the comparison that will trigger a validator """
        config = json.loads(self.validator_config)

        if self.validator_type.lower() == "operator":
            return f"{config['op']} {config['threshold']}"

        if self.validator_type.lower() == "not null":
            return "!= Null or 0"

        return ""


class AlertLog(Model):
    """更改提醒日志对象关系模型。"""

    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True)
    scheduled_dttm = Column(DateTime)
    dttm_start = Column(DateTime, default=datetime.utcnow)
    dttm_end = Column(DateTime, default=datetime.utcnow)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    alert = relationship("Alert", backref="logs", foreign_keys=[alert_id])
    state = Column(String(10))

    @property
    def duration(self) -> int:
        return (self.dttm_end - self.dttm_start).total_seconds()


class SQLObservation(Model):
    """更改提醒观察对象关系模型。"""

    __tablename__ = "sql_observations"

    id = Column(Integer, primary_key=True)
    dttm = Column(DateTime, default=datetime.utcnow, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    alert = relationship(
        "Alert",
        foreign_keys=[alert_id],
        backref=backref("observations", cascade="all, delete-orphan"),
    )
    value = Column(Float)
    error_msg = Column(String(500))
