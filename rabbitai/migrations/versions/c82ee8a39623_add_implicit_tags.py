"""Add implicit tags

Revision ID: c82ee8a39623
Revises: c18bd4186f15
Create Date: 2018-07-26 11:10:23.653524

"""

# revision identifiers, used by Alembic.
revision = "c82ee8a39623"
down_revision = "c617da68de7d"

from alembic import op
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from rabbitai.models.helpers import AuditMixinNullable
from rabbitai.models.tags import ObjectTypes, TagTypes

Base = declarative_base()


class Tag(Base, AuditMixinNullable):
    """A tag attached to an object (query, chart or dashboard)."""

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    type = Column(Enum(TagTypes))


class TaggedObject(Base, AuditMixinNullable):
    __tablename__ = "tagged_object"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"))
    object_id = Column(Integer)
    object_type = Column(Enum(ObjectTypes))


class User(Base):
    """Declarative class to do query in upgrade"""

    __tablename__ = "ab_user"
    id = Column(Integer, primary_key=True)


def upgrade():
    bind = op.get_bind()
    Tag.__table__.create(bind)
    TaggedObject.__table__.create(bind)


def downgrade():
    op.drop_table("tagged_object")
    op.drop_table("tag")
