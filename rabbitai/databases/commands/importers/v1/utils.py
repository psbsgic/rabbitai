import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from rabbitai.models.core import Database


def import_database(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> Database:
    """
    将指定配置字典中的内容导入到数据库。

    :param session: 数据库会话。
    :param config: 配置字典。
    :param overwrite: 是否重写。
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
