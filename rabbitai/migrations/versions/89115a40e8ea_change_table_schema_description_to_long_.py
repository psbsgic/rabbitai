"""Change table schema description to long text

Revision ID: 89115a40e8ea
Revises: 5afa9079866a
Create Date: 2019-12-03 13:50:24.746867

"""

# revision identifiers, used by Alembic.
revision = "89115a40e8ea"
down_revision = "5afa9079866a"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.databases import mysql
from sqlalchemy.dialects.mysql.base import MySQLDialect


def upgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table("table_schema") as batch_op:
            batch_op.alter_column(
                "description", existing_type=sa.Text, type_=mysql.LONGTEXT
            )


def downgrade():
    bind = op.get_bind()
    if isinstance(bind.dialect, MySQLDialect):
        with op.batch_alter_table("table_schema") as batch_op:
            batch_op.alter_column(
                "description", existing_type=mysql.LONGTEXT, type_=sa.Text
            )
