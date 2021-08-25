from typing import Any, Dict, Set

from marshmallow import Schema
from sqlalchemy.orm import Session

from rabbitai.commands.importers.v1 import ImportModelsCommand
from rabbitai.databases.commands.importers.v1.utils import import_database
from rabbitai.databases.schemas import ImportV1DatabaseSchema
from rabbitai.datasets.commands.exceptions import DatasetImportError
from rabbitai.datasets.commands.importers.v1.utils import import_dataset
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.datasets.schemas import ImportV1DatasetSchema


class ImportDatasetsCommand(ImportModelsCommand):
    """Import datasets"""

    dao = DatasetDAO
    model_name = "dataset"
    prefix = "datasets/"
    schemas: Dict[str, Schema] = {
        "databases/": ImportV1DatabaseSchema(),
        "datasets/": ImportV1DatasetSchema(),
    }
    import_error = DatasetImportError

    @staticmethod
    def _import(
        session: Session, configs: Dict[str, Any], overwrite: bool = False
    ) -> None:
        # discover databases associated with datasets
        database_uuids: Set[str] = set()
        for file_name, config in configs.items():
            if file_name.startswith("datasets/"):
                database_uuids.add(config["database_uuid"])

        # import related databases
        database_ids: Dict[str, int] = {}
        for file_name, config in configs.items():
            if file_name.startswith("databases/") and config["uuid"] in database_uuids:
                database = import_database(session, config, overwrite=False)
                database_ids[str(database.uuid)] = database.id

        # import datasets with the correct parent ref
        for file_name, config in configs.items():
            if (
                file_name.startswith("datasets/")
                and config["database_uuid"] in database_ids
            ):
                config["database_id"] = database_ids[config["database_uuid"]]
                import_dataset(session, config, overwrite=overwrite)
