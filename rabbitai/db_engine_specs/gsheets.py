from typing import Optional

from sqlalchemy.engine.url import URL

from rabbitai import security_manager
from rabbitai.db_engine_specs.sqlite import SqliteEngineSpec


class GSheetsEngineSpec(SqliteEngineSpec):
    """Engine for Google spreadsheets"""

    engine = "gsheets"
    engine_name = "Google Sheets"
    allows_joins = False
    allows_subqueries = True

    @classmethod
    def modify_url_for_impersonation(
        cls, url: URL, impersonate_user: bool, username: Optional[str]
    ) -> None:
        if impersonate_user and username is not None:
            user = security_manager.find_user(username=username)
            if user and user.email:
                url.query["subject"] = user.email
