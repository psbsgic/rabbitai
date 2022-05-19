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
    """
    导出对象关系模型命令，默认生成 metadata.yaml 文件和内容，文件名称和文件内容（模型数据）。

    派生类必须重写 _export(model: Model) 方法以实现将对象关系模型数据存储到文件的逻辑。
    """

    dao = BaseDAO
    not_found = CommandException

    def __init__(self, model_ids: List[int]):
        """
        使用指定数据模型标识的列表，初始化新实例。

        :param model_ids: 数据模型标识的列表。
        """

        self.model_ids = model_ids

        # this will be set when calling validate()
        self._models: List[Model] = []

    @staticmethod
    def _export(model: Model) -> Iterator[Tuple[str, str]]:
        """
        派生类重写，导出指定数据模型到文件。

        :param model: 数据模型。
        :return:
        """
        raise NotImplementedError("Subclasses MUST implement _export")

    def run(self) -> Iterator[Tuple[str, str]]:
        """
        执行该命令。

        - 调用 validate() 方法进行验证
        - 构建元数据并导出到文件
        - 导出每个模型到文件，期间调用 _export 方法

        :return: 文件名称，文件内容元组的迭代器。
        """
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
        """验证能否执行该命令，如果不满足条件则引发异常。"""

        self._models = self.dao.find_by_ids(self.model_ids)
        if len(self._models) != len(self.model_ids):
            raise self.not_found()
