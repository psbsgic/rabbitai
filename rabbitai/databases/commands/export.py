# -*- coding: utf-8 -*-

import json
import logging
from typing import Any, Dict, Iterator, Tuple

import yaml
from werkzeug.utils import secure_filename

from rabbitai.databases.commands.exceptions import DatabaseNotFoundError
from rabbitai.databases.dao import DatabaseDAO
from rabbitai.commands.export import ExportModelsCommand
from rabbitai.models.core import Database
from rabbitai.utils.dict_import_export import EXPORT_VERSION

logger = logging.getLogger(__name__)


def parse_extra(extra_payload: str) -> Dict[str, Any]:
    try:
        extra = json.loads(extra_payload)
    except json.decoder.JSONDecodeError:
        logger.info("Unable to decode `extra` field: %s", extra_payload)
        return {}

    # Fix for DBs saved with an invalid ``schemas_allowed_for_csv_upload``
    schemas_allowed_for_csv_upload = extra.get("schemas_allowed_for_csv_upload")
    if isinstance(schemas_allowed_for_csv_upload, str):
        extra["schemas_allowed_for_csv_upload"] = json.loads(
            schemas_allowed_for_csv_upload
        )

    return extra


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
            payload["extra"] = parse_extra(payload["extra"])

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
