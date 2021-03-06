"""add_slack_to_alerts

Revision ID: f2672aa8350a
Revises: 2f1d15e8a6af
Create Date: 2020-08-08 18:10:51.973551

"""

# revision identifiers, used by Alembic.
revision = "f2672aa8350a"
down_revision = "2f1d15e8a6af"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("alerts", sa.Column("slack_channel", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("alerts", "slack_channel")
    # ### end Alembic commands ###
