"""cleanup_time_grainularity

Revision ID: f9a30386bd74
Revises: b5998378c225
Create Date: 2020-03-25 10:42:11.047328

"""

# revision identifiers, used by Alembic.
revision = "f9a30386bd74"
down_revision = "b5998378c225"

import json

from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from rabbitai import db

Base = declarative_base()


class Slice(Base):
    __tablename__ = "slices"

    id = Column(Integer, primary_key=True)
    params = Column(Text)
    viz_type = Column(String(250))


def upgrade():
    """
    Remove any erroneous time grainularity fields from slices foor those visualization
    types which do not support time granularity.

    :see: https://github.com/apache/rabbitai/pull/8674
    :see: https://github.com/apache/rabbitai/pull/8764
    :see: https://github.com/apache/rabbitai/pull/8800
    :see: https://github.com/apache/rabbitai/pull/8825
    """

    bind = op.get_bind()
    session = db.Session(bind=bind)

    # Visualization types which support time grainularity (hence negate).
    viz_types = [
        "area",
        "bar",
        "big_number",
        "compare",
        "dual_line",
        "line",
        "pivot_table",
        "table",
        "time_pivot",
        "time_table",
    ]

    # Erroneous time grainularity fields for either Druid NoSQL or SQL slices which do
    # not support time grainularity.
    erroneous = ["grainularity", "time_grain_sqla"]

    for slc in session.query(Slice).filter(Slice.viz_type.notin_(viz_types)).all():
        try:
            params = json.loads(slc.params)

            if any(field in params for field in erroneous):
                for field in erroneous:
                    if field in params:
                        del params[field]

                slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    pass
