"""allow_dml

Revision ID: 65903709c321
Revises: 4500485bde7d
Create Date: 2016-09-15 08:48:27.284752

"""

import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "65903709c321"
down_revision = "4500485bde7d"


def upgrade():
    op.add_column("dbs", sa.Column("allow_dml", sa.Boolean(), nullable=True))


def downgrade():
    try:
        op.drop_column("dbs", "allow_dml")
    except Exception as ex:
        logging.exception(ex)
        pass
