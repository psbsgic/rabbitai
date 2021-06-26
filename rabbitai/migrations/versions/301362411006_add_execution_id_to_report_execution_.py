"""add_execution_id_to_report_execution_log_model.py

Revision ID: 301362411006
Revises: 989bbe479899
Create Date: 2021-03-23 05:23:15.641856

"""

# revision identifiers, used by Alembic.
revision = "301362411006"
down_revision = "989bbe479899"

import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import UUIDType


def upgrade():
    op.add_column("report_execution_log", sa.Column("uuid", UUIDType(binary=True)))


def downgrade():
    op.drop_column("report_execution_log", "execution_id")
