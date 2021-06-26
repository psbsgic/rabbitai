from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.models.sql_lab import SavedQuery


def import_saved_query(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> SavedQuery:
    existing = session.query(SavedQuery).filter_by(uuid=config["uuid"]).first()
    if existing:
        if not overwrite:
            return existing
        config["id"] = existing.id

    saved_query = SavedQuery.import_from_dict(session, config, recursive=False)
    if saved_query.id is None:
        session.flush()

    return saved_query
