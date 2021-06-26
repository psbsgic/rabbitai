# isort:skip_file

import json
import logging
from typing import Iterator, Tuple

import yaml
from werkzeug.utils import secure_filename

from rabbitai.commands.export import ExportModelsCommand
from rabbitai.models.sql_lab import SavedQuery
from rabbitai.queries.saved_queries.commands.exceptions import SavedQueryNotFoundError
from rabbitai.queries.saved_queries.dao import SavedQueryDAO
from rabbitai.utils.dict_import_export import EXPORT_VERSION

logger = logging.getLogger(__name__)


class ExportSavedQueriesCommand(ExportModelsCommand):

    dao = SavedQueryDAO
    not_found = SavedQueryNotFoundError

    @staticmethod
    def _export(model: SavedQuery) -> Iterator[Tuple[str, str]]:
        # build filename based on database, optional schema, and label
        database_slug = secure_filename(model.database.database_name)
        schema_slug = secure_filename(model.schema)
        query_slug = secure_filename(model.label) or str(model.uuid)
        file_name = f"queries/{database_slug}/{schema_slug}/{query_slug}.yaml"

        payload = model.export_to_dict(
            recursive=False,
            include_parent_ref=False,
            include_defaults=True,
            export_uuids=True,
        )
        payload["version"] = EXPORT_VERSION
        payload["database_uuid"] = str(model.database.uuid)

        file_content = yaml.safe_dump(payload, sort_keys=False)
        yield file_name, file_content

        # include database as well
        file_name = f"databases/{database_slug}.yaml"

        payload = model.database.export_to_dict(
            recursive=False,
            include_parent_ref=False,
            include_defaults=True,
            export_uuids=True,
        )
        # TODO (betodealmeida): move this logic to export_to_dict once this
        # becomes the default export endpoint
        if "extra" in payload:
            try:
                payload["extra"] = json.loads(payload["extra"])
            except json.decoder.JSONDecodeError:
                logger.info("Unable to decode `extra` field: %s", payload["extra"])

        payload["version"] = EXPORT_VERSION

        file_content = yaml.safe_dump(payload, sort_keys=False)
        yield file_name, file_content
