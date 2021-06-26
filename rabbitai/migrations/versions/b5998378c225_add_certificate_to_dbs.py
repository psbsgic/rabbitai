"""add certificate to dbs

Revision ID: b5998378c225
Revises: 72428d1ea401
Create Date: 2020-03-25 10:49:10.883065

"""

# revision identifiers, used by Alembic.
revision = "b5998378c225"
down_revision = "72428d1ea401"

from typing import Dict

import sqlalchemy as sa
from alembic import op


def upgrade():
    kwargs: Dict[str, str] = {}
    bind = op.get_bind()
    op.add_column(
        "dbs", sa.Column("server_cert", sa.LargeBinary(), nullable=True, **kwargs),
    )


def downgrade():
    op.drop_column("dbs", "server_cert")
