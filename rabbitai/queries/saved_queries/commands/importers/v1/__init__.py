from typing import Any, Dict, Set

from marshmallow import Schema
from sqlalchemy.orm import Session

from rabbitai.commands.importers.v1 import ImportModelsCommand
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.databases.commands.importers.v1.utils import import_database
from rabbitai.databases.schemas import ImportV1DatabaseSchema
from rabbitai.queries.saved_queries.commands.exceptions import SavedQueryImportError
from rabbitai.queries.saved_queries.commands.importers.v1.utils import (
    import_saved_query,
)
from rabbitai.queries.saved_queries.dao import SavedQueryDAO
from rabbitai.queries.saved_queries.schemas import ImportV1SavedQuerySchema


class ImportSavedQueriesCommand(ImportModelsCommand):
    """导入保存的查询命令。"""

    dao = SavedQueryDAO
    model_name = "saved_queries"
    prefix = "queries/"
    schemas: Dict[str, Schema] = {
        "databases/": ImportV1DatabaseSchema(),
        "queries/": ImportV1SavedQuerySchema(),
    }
    import_error = SavedQueryImportError

    @staticmethod
    def _import(
        session: Session, configs: Dict[str, Any], overwrite: bool = False
    ) -> None:
        # discover databases associated with saved queries
        database_uuids: Set[str] = set()
        for file_name, config in configs.items():
            if file_name.startswith("queries/"):
                database_uuids.add(config["database_uuid"])

        # import related databases
        database_ids: Dict[str, int] = {}
        for file_name, config in configs.items():
            if file_name.startswith("databases/") and config["uuid"] in database_uuids:
                database = import_database(session, config, overwrite=False)
                database_ids[str(database.uuid)] = database.id

        # import saved queries with the correct parent ref
        for file_name, config in configs.items():
            if (
                file_name.startswith("queries/")
                and config["database_uuid"] in database_ids
            ):
                config["db_id"] = database_ids[config["database_uuid"]]
                import_saved_query(session, config, overwrite=overwrite)
