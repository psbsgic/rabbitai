import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.models.slice import Slice


def import_chart(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> Slice:
    existing = session.query(Slice).filter_by(uuid=config["uuid"]).first()
    if existing:
        if not overwrite:
            return existing
        config["id"] = existing.id

    # TODO (betodealmeida): move this logic to import_from_dict
    config["params"] = json.dumps(config["params"])

    chart = Slice.import_from_dict(session, config, recursive=False)
    if chart.id is None:
        session.flush()

    return chart
