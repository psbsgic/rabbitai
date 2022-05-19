# isort:skip_file

import json
import logging
from typing import Iterator, Tuple

import yaml
from werkzeug.utils import secure_filename

from rabbitai.commands.export import ExportModelsCommand
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.datasets.commands.exceptions import DatasetNotFoundError
from rabbitai.datasets.dao import DatasetDAO
from rabbitai.utils.dict_import_export import EXPORT_VERSION

logger = logging.getLogger(__name__)

JSON_KEYS = {"params", "template_params"}


class ExportDatasetsCommand(ExportModelsCommand):
    """导出数据集命令，将数据集输出到文件：datasets/{database_slug}/{dataset_slug}.yaml。
    执行命令生成：file_name, file_content。"""

    dao = DatasetDAO
    not_found = DatasetNotFoundError

    @staticmethod
    def _export(model: SqlaTable) -> Iterator[Tuple[str, str]]:
        database_slug = secure_filename(model.database.database_name)
        dataset_slug = secure_filename(model.table_name)
        file_name = f"datasets/{database_slug}/{dataset_slug}.yaml"

        payload = model.export_to_dict(
            recursive=True,
            include_parent_ref=False,
            include_defaults=True,
            export_uuids=True,
        )

        for key in JSON_KEYS:
            if payload.get(key):
                try:
                    payload[key] = json.loads(payload[key])
                except json.decoder.JSONDecodeError:
                    logger.info("Unable to decode `%s` field: %s", key, payload[key])

        for metric in payload.get("metrics", []):
            if metric.get("extra"):
                try:
                    metric["extra"] = json.loads(metric["extra"])
                except json.decoder.JSONDecodeError:
                    logger.info("Unable to decode `extra` field: %s", metric["extra"])

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

        if payload.get("extra"):
            try:
                payload["extra"] = json.loads(payload["extra"])
            except json.decoder.JSONDecodeError:
                logger.info("Unable to decode `extra` field: %s", payload["extra"])

        payload["version"] = EXPORT_VERSION

        file_content = yaml.safe_dump(payload, sort_keys=False)

        yield file_name, file_content
