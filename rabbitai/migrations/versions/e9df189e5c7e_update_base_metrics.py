"""update base metrics

Note that the metrics table was previously partially modifed by revision
f231d82b9b26.

Revision ID: e9df189e5c7e
Revises: 7f2635b51f5d
Create Date: 2018-07-20 15:57:48.118304

"""

# revision identifiers, used by Alembic.
revision = "e9df189e5c7e"
down_revision = "7f2635b51f5d"

from alembic import op
from sqlalchemy import Column, engine, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from rabbitai import db
from rabbitai.utils.core import generic_find_uq_constraint_name

Base = declarative_base()

conv = {"uq": "uq_%(table_name)s_%(column_0_name)s"}


class BaseMetricMixin:
    id = Column(Integer, primary_key=True)


class DruidMetric(BaseMetricMixin, Base):
    __tablename__ = "metrics"

    datasource_id = Column(Integer)


class SqlMetric(BaseMetricMixin, Base):
    __tablename__ = "sql_metrics"

    table_id = Column(Integer)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)

    # Delete the orphaned metrics records.
    for record in session.query(DruidMetric).all():
        if record.datasource_id is None:
            session.delete(record)

    session.commit()

    # Enforce that metrics.metric_name column be non-nullable.
    with op.batch_alter_table("metrics") as batch_op:
        batch_op.alter_column("metric_name", existing_type=String(255), nullable=False)

    # Enforce that metrics.json column be non-nullable.
    with op.batch_alter_table("metrics") as batch_op:
        batch_op.alter_column("json", existing_type=Text, nullable=False)

    # Delete the orphaned sql_metrics records.
    for record in session.query(SqlMetric).all():
        if record.table_id is None:
            session.delete(record)

    session.commit()

    # Reduce the size of the sql_metrics.metric_name column for constraint
    # viability and enforce that it to be non-nullable.
    with op.batch_alter_table("sql_metrics") as batch_op:
        batch_op.alter_column(
            "metric_name", existing_type=String(512), nullable=False, type_=String(255)
        )

    # Enforce that sql_metrics.expression column be non-nullable.
    with op.batch_alter_table("sql_metrics") as batch_op:
        batch_op.alter_column("expression", existing_type=Text, nullable=False)

    # Add the missing uniqueness constraint to the sql_metrics table.
    with op.batch_alter_table("sql_metrics", naming_convention=conv) as batch_op:
        batch_op.create_unique_constraint(
            "uq_sql_metrics_metric_name", ["metric_name", "table_id"]
        )


def downgrade():
    bind = op.get_bind()
    insp = engine.reflection.Inspector.from_engine(bind)

    # Remove the missing uniqueness constraint from the sql_metrics table.
    with op.batch_alter_table("sql_metrics", naming_convention=conv) as batch_op:
        batch_op.drop_constraint(
            generic_find_uq_constraint_name(
                "sql_metrics", {"metric_name", "table_id"}, insp
            )
            or "uq_sql_metrics_table_id",
            type_="unique",
        )

    # Restore the size of the sql_metrics.metric_name column and forego that it
    # be non-nullable.
    with op.batch_alter_table("sql_metrics") as batch_op:
        batch_op.alter_column(
            "metric_name", existing_type=String(255), nullable=True, type_=String(512)
        )

    # Forego that the sql_metrics.expression column be non-nullable.
    with op.batch_alter_table("sql_metrics") as batch_op:
        batch_op.alter_column("expression", existing_type=Text, nullable=True)

    # Forego that the metrics.metric_name column be non-nullable.
    with op.batch_alter_table("metrics") as batch_op:
        batch_op.alter_column("metric_name", existing_type=String(255), nullable=True)

    # Forego that the metrics.json column be non-nullable.
    with op.batch_alter_table("metrics") as batch_op:
        batch_op.alter_column("json", existing_type=Text, nullable=True)
