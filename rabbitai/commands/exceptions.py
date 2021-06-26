from typing import Any, Dict, List

from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from rabbitai.exceptions import RabbitaiException


class CommandException(RabbitaiException):
    """ Common base class for Command exceptions. """

    def __repr__(self) -> str:
        if self._exception:
            return repr(self._exception)
        return repr(self)


class CommandInvalidError(CommandException):
    """ Common base class for Command Invalid errors. """

    status = 422

    def __init__(self, message: str = "") -> None:
        self._invalid_exceptions: List[ValidationError] = []
        super().__init__(message)

    def add(self, exception: ValidationError) -> None:
        self._invalid_exceptions.append(exception)

    def add_list(self, exceptions: List[ValidationError]) -> None:
        self._invalid_exceptions.extend(exceptions)

    def normalized_messages(self) -> Dict[Any, Any]:
        errors: Dict[Any, Any] = {}
        for exception in self._invalid_exceptions:
            errors.update(exception.normalized_messages())
        return errors


class UpdateFailedError(CommandException):
    status = 500
    message = "Command update failed"


class CreateFailedError(CommandException):
    status = 500
    message = "Command create failed"


class DeleteFailedError(CommandException):
    status = 500
    message = "Command delete failed"


class ForbiddenError(CommandException):
    status = 403
    message = "Action is forbidden"


class ImportFailedError(CommandException):
    status = 500
    message = "Import failed for an unknown reason"


class OwnersNotFoundValidationError(ValidationError):
    status = 422

    def __init__(self) -> None:
        super().__init__([_("Owners are invalid")], field_name="owners")


class RolesNotFoundValidationError(ValidationError):
    status = 422

    def __init__(self) -> None:
        super().__init__([_("Some roles do not exist")], field_name="roles")


class DatasourceNotFoundValidationError(ValidationError):
    status = 404

    def __init__(self) -> None:
        super().__init__([_("Dataset does not exist")], field_name="datasource_id")
