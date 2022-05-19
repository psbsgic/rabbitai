from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """
    命令抽象基类，所有 RabbitAI 命令都继承该类。

    定义派生类必须重写的两个方法：

    - run()
    - validate()：验证可否满足执行命令的条件，如果不满足则引发异常。
    """

    @abstractmethod
    def run(self) -> Any:
        """
        执行该命令，可能引发命令异常。
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        验证可否满足执行命令的条件，如果不满足则引发异常。

        :raises: CommandException
        """
