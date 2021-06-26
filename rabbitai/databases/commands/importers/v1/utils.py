import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.models.core import Database


def import_database(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> Database:
    existing = session.query(Database).filter_by(uuid=config["uuid"]).first()
    if existing:
        if not overwrite:
            return existing
        config["id"] = existing.id

    # TODO (betodealmeida): move this logic to import_from_dict
    config["extra"] = json.dumps(config["extra"])

    database = Database.import_from_dict(session, config, recursive=False)
    if database.id is None:
        session.flush()

    return database
