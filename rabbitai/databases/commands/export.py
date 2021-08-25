# isort:skip_file

import json
import logging
from typing import Iterator, Tuple

import yaml
from werkzeug.utils import secure_filename

from rabbitai.databases.commands.exceptions import DatabaseNotFoundError
from rabbitai.databases.dao import DatabaseDAO
from rabbitai.commands.export import ExportModelsCommand
from rabbitai.models.core import Database
from rabbitai.utils.dict_import_export import EXPORT_VERSION

logger = logging.getLogger(__name__)


class ExportDatabasesCommand(ExportModelsCommand):

    dao = DatabaseDAO
    not_found = DatabaseNotFoundError

    @staticmethod
    def _export(model: Database) -> Iterator[Tuple[str, str]]:
        database_slug = secure_filename(model.database_name)
        file_name = f"databases/{database_slug}.yaml"

        payload = model.export_to_dict(
            recursive=False,
            include_parent_ref=False,
            include_defaults=True,
            export_uuids=True,
        )

        if payload.get("extra"):
            try:
                payload["extra"] = json.loads(payload["extra"])
            except json.decoder.JSONDecodeError:
                logger.info("Unable to decode `extra` field: %s", payload["extra"])

        payload["version"] = EXPORT_VERSION

        file_content = yaml.safe_dump(payload, sort_keys=False)
        yield file_name, file_content

        for dataset in model.tables:
            dataset_slug = secure_filename(dataset.table_name)
            file_name = f"datasets/{database_slug}/{dataset_slug}.yaml"

            payload = dataset.export_to_dict(
                recursive=True,
                include_parent_ref=False,
                include_defaults=True,
                export_uuids=True,
            )
            payload["version"] = EXPORT_VERSION
            payload["database_uuid"] = str(model.uuid)

            file_content = yaml.safe_dump(payload, sort_keys=False)
            yield file_name, file_content
