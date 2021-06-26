"""security converge annotations

Revision ID: c25cb2c78727
Revises: ccb74baaa89b
Create Date: 2020-12-11 17:02:21.213046

"""

from alembic import op
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
from rabbitai.migrations.shared.security_converge import (
    add_pvms,
    get_reversed_new_pvms,
    get_reversed_pvm_map,
    migrate_roles,
    Pvm,
)

revision = "c25cb2c78727"
down_revision = "ccb74baaa89b"


NEW_PVMS = {"Annotation": ("can_read", "can_write",)}
PVM_MAP = {
    Pvm("AnnotationLayerModelView", "can_delete"): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationLayerModelView", "can_list"): (Pvm("Annotation", "can_read"),),
    Pvm("AnnotationLayerModelView", "can_show",): (Pvm("Annotation", "can_read"),),
    Pvm("AnnotationLayerModelView", "can_add",): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationLayerModelView", "can_edit",): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationModelView", "can_annotation",): (Pvm("Annotation", "can_read"),),
    Pvm("AnnotationModelView", "can_show",): (Pvm("Annotation", "can_read"),),
    Pvm("AnnotationModelView", "can_add",): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationModelView", "can_delete",): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationModelView", "can_edit",): (Pvm("Annotation", "can_write"),),
    Pvm("AnnotationModelView", "can_list",): (Pvm("Annotation", "can_read"),),
}


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Add the new permissions on the migration itself
    add_pvms(session, NEW_PVMS)
    migrate_roles(session, PVM_MAP)
    try:
        session.commit()
    except SQLAlchemyError as ex:
        print(f"An error occurred while upgrading annotation permissions: {ex}")
        session.rollback()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Add the old permissions on the migration itself
    add_pvms(session, get_reversed_new_pvms(PVM_MAP))
    migrate_roles(session, get_reversed_pvm_map(PVM_MAP))
    try:
        session.commit()
    except SQLAlchemyError as ex:
        print(f"An error occurred while downgrading annotation permissions: {ex}")
        session.rollback()
    pass