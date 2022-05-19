import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.models.core import Database


def import_database(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> Database:
    """
    导入数据库到数据库。

    :param session: 数据库会话。
    :param config: 包含要导入数据库相关配置信息。
    :param overwrite:
    :return:
    """

    existing = session.query(Database).filter_by(uuid=config["uuid"]).first()
    if existing:
        if not overwrite:
            return existing
        config["id"] = existing.id

    config["extra"] = json.dumps(config["extra"])

    database = Database.import_from_dict(session, config, recursive=False)
    if database.id is None:
        session.flush()

    return database
