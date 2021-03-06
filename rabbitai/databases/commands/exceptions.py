# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _
from marshmallow.validate import ValidationError

from rabbitai.commands.exceptions import (
    CommandException,
    CommandInvalidError,
    CreateFailedError,
    DeleteFailedError,
    ImportFailedError,
    UpdateFailedError,
)
from rabbitai.exceptions import RabbitaiErrorException, RabbitaiErrorsException


class DatabaseInvalidError(CommandInvalidError):
    message = _("Database parameters are invalid.")


class DatabaseExistsValidationError(ValidationError):
    """
    Marshmallow validation error for dataset already exists
    """

    def __init__(self) -> None:
        super().__init__(
            _("A database with the same name already exists."),
            field_name="database_name",
        )


class DatabaseRequiredFieldValidationError(ValidationError):
    def __init__(self, field_name: str) -> None:
        super().__init__(
            [_("Field is required")], field_name=field_name,
        )


class DatabaseExtraJSONValidationError(ValidationError):
    """
    Marshmallow validation error for database encrypted extra must be a valid JSON
    """

    def __init__(self, json_error: str = "") -> None:
        super().__init__(
            [
                _(
                    "Field cannot be decoded by JSON.  %{json_error}s",
                    json_error=json_error,
                )
            ],
            field_name="extra",
        )


class DatabaseExtraValidationError(ValidationError):
    """
    Marshmallow validation error for database encrypted extra must be a valid JSON
    """

    def __init__(self, key: str = "") -> None:
        super().__init__(
            [
                _(
                    "The metadata_params in Extra field "
                    "is not configured correctly. The key "
                    "%{key}s is invalid.",
                    key=key,
                )
            ],
            field_name="extra",
        )


class DatabaseNotFoundError(CommandException):
    message = _("Database not found.")


class DatabaseCreateFailedError(CreateFailedError):
    message = _("Database could not be created.")


class DatabaseUpdateFailedError(UpdateFailedError):
    message = _("Database could not be updated.")


class DatabaseConnectionFailedError(  # pylint: disable=too-many-ancestors
    DatabaseCreateFailedError, DatabaseUpdateFailedError,
):
    message = _("Connection failed, please check your connection settings")


class DatabaseDeleteDatasetsExistFailedError(DeleteFailedError):
    message = _("Cannot delete a database that has datasets attached")


class DatabaseDeleteFailedError(DeleteFailedError):
    message = _("Database could not be deleted.")


class DatabaseDeleteFailedReportsExistError(DatabaseDeleteFailedError):
    message = _("There are associated alerts or reports")


class DatabaseTestConnectionFailedError(RabbitaiErrorsException):
    status = 422
    message = _("Connection failed, please check your connection settings")


class DatabaseSecurityUnsafeError(CommandInvalidError):
    message = _("Stopped an unsafe database connection")


class DatabaseTestConnectionDriverError(CommandInvalidError):
    message = _("Could not load database driver")


class DatabaseTestConnectionUnexpectedError(RabbitaiErrorsException):
    status = 422
    message = _("Unexpected error occurred, please check your logs for details")


class DatabaseImportError(ImportFailedError):
    message = _("Import database failed for an unknown reason")


class InvalidEngineError(RabbitaiErrorException):
    status = 422


class DatabaseOfflineError(RabbitaiErrorException):
    status = 422


class InvalidParametersError(RabbitaiErrorsException):
    status = 422
