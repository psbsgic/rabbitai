from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """命令抽象基类，定义方法：run、validate。"""

    @abstractmethod
    def run(self) -> Any:
        """
        执行该命令。如果失败触发异常，
        :raises: CommandException。
        """

    @abstractmethod
    def validate(self) -> None:
        """
        在执行命令前验证数据的有效性，如果验证失败则触发异常，
        :raises: CommandException。
        """
