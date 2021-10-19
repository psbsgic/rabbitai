from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    """
        Base class for all Command like Rabbitai Logic objects
    """

    @abstractmethod
    def run(self) -> Any:
        """
        Run executes the command. Can raise command exceptions
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate is normally called by run to validate data.
        Will raise exception if validation fails
        :raises: CommandException
        """
