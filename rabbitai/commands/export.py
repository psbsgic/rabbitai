# isort:skip_file

from datetime import datetime
from datetime import timezone
from typing import Iterator, List, Tuple

import yaml
from flask_appbuilder import Model

from rabbitai.commands.base import BaseCommand
from rabbitai.commands.exceptions import CommandException
from rabbitai.dao.base import BaseDAO
from rabbitai.utils.dict_import_export import EXPORT_VERSION

METADATA_FILE_NAME = "metadata.yaml"


class ExportModelsCommand(BaseCommand):

    dao = BaseDAO
    not_found = CommandException

    def __init__(self, model_ids: List[int]):
        self.model_ids = model_ids

        # this will be set when calling validate()
        self._models: List[Model] = []

    @staticmethod
    def _export(model: Model) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError("Subclasses MUST implement _export")

    def run(self) -> Iterator[Tuple[str, str]]:
        self.validate()

        metadata = {
            "version": EXPORT_VERSION,
            "type": self.dao.model_cls.__name__,  # type: ignore
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }
        yield METADATA_FILE_NAME, yaml.safe_dump(metadata, sort_keys=False)

        seen = {METADATA_FILE_NAME}
        for model in self._models:
            for file_name, file_content in self._export(model):
                if file_name not in seen:
                    yield file_name, file_content
                    seen.add(file_name)

    def validate(self) -> None:
        self._models = self.dao.find_by_ids(self.model_ids)
        if len(self._models) != len(self.model_ids):
            raise self.not_found()
