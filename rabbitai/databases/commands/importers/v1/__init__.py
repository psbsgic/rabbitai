from typing import Any, Dict

from marshmallow import Schema
from sqlalchemy.orm import Session

from rabbitai.commands.importers.v1 import ImportModelsCommand
from rabbitai.databases.commands.exceptions import DatabaseImportError
from rabbitai.databases.commands.importers.v1.utils import import_database
from rabbitai.databases.dao import DatabaseDAO
from rabbitai.databases.schemas import ImportV1DatabaseSchema
from rabbitai.datasets.commands.importers.v1.utils import import_dataset
from rabbitai.datasets.schemas import ImportV1DatasetSchema


class ImportDatabasesCommand(ImportModelsCommand):
    """导入数据库对象模型到数据库的命令。"""

    dao = DatabaseDAO
    model_name = "database"
    prefix = "databases/"
    schemas: Dict[str, Schema] = {
        "databases/": ImportV1DatabaseSchema(),
        "datasets/": ImportV1DatasetSchema(),
    }
    import_error = DatabaseImportError

    @staticmethod
    def _import(
        session: Session, configs: Dict[str, Any], overwrite: bool = False
    ) -> None:
        # first import databases
        database_ids: Dict[str, int] = {}
        for file_name, config in configs.items():
            if file_name.startswith("databases/"):
                database = import_database(session, config, overwrite=overwrite)
                database_ids[str(database.uuid)] = database.id

        # import related datasets
        for file_name, config in configs.items():
            if (
                file_name.startswith("datasets/")
                and config["database_uuid"] in database_ids
            ):
                config["database_id"] = database_ids[config["database_uuid"]]
                # overwrite=False prevents deleting any non-imported columns/metrics
                import_dataset(session, config, overwrite=False)
