# isort:skip_file

import json
import logging
from typing import Iterator, Tuple

import yaml
from werkzeug.utils import secure_filename

from rabbitai.charts.commands.exceptions import ChartNotFoundError
from rabbitai.charts.dao import ChartDAO
from rabbitai.datasets.commands.export import ExportDatasetsCommand
from rabbitai.commands.export import ExportModelsCommand
from rabbitai.models.slice import Slice
from rabbitai.utils.dict_import_export import EXPORT_VERSION

logger = logging.getLogger(__name__)


# keys present in the standard export that are not needed
REMOVE_KEYS = ["datasource_type", "datasource_name"]


class ExportChartsCommand(ExportModelsCommand):
    """导出图表对象关系模型到文件的命令。"""

    dao = ChartDAO
    not_found = ChartNotFoundError

    @staticmethod
    def _export(model: Slice) -> Iterator[Tuple[str, str]]:
        chart_slug = secure_filename(model.slice_name)
        file_name = f"charts/{chart_slug}_{model.id}.yaml"

        payload = model.export_to_dict(
            recursive=False,
            include_parent_ref=False,
            include_defaults=True,
            export_uuids=True,
        )

        for key in REMOVE_KEYS:
            del payload[key]
        if payload.get("params"):
            try:
                payload["params"] = json.loads(payload["params"])
            except json.decoder.JSONDecodeError:
                logger.info("Unable to decode `params` field: %s", payload["params"])

        payload["version"] = EXPORT_VERSION
        if model.table:
            payload["dataset_uuid"] = str(model.table.uuid)

        file_content = yaml.safe_dump(payload, sort_keys=False)
        yield file_name, file_content

        if model.table:
            yield from ExportDatasetsCommand([model.table.id]).run()
