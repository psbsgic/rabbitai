from flask_babel import lazy_gettext as _
from marshmallow.validate import ValidationError

from rabbitai.commands.exceptions import (
    CommandException,
    CommandInvalidError,
    CreateFailedError,
    DeleteFailedError,
    ForbiddenError,
    ImportFailedError,
    UpdateFailedError,
)


class DashboardSlugExistsValidationError(ValidationError):
    """
    Marshmallow validation error for dashboard slug already exists
    """

    def __init__(self) -> None:
        super().__init__([_("Must be unique")], field_name="slug")


class DashboardInvalidError(CommandInvalidError):
    message = _("Dashboard parameters are invalid.")


class DashboardNotFoundError(CommandException):
    message = _("Dashboard not found.")


class DashboardCreateFailedError(CreateFailedError):
    message = _("Dashboard could not be created.")


class DashboardBulkDeleteFailedError(CreateFailedError):
    message = _("Dashboards could not be deleted.")


class DashboardBulkDeleteFailedReportsExistError(DashboardBulkDeleteFailedError):
    message = _("There are associated alerts or reports")


class DashboardUpdateFailedError(UpdateFailedError):
    message = _("Dashboard could not be updated.")


class DashboardDeleteFailedError(DeleteFailedError):
    message = _("Dashboard could not be deleted.")


class DashboardDeleteFailedReportsExistError(DashboardDeleteFailedError):
    message = _("There are associated alerts or reports")


class DashboardForbiddenError(ForbiddenError):
    message = _("Changing this Dashboard is forbidden")


class DashboardImportError(ImportFailedError):
    message = _("Import dashboard failed for an unknown reason")


class DashboardAccessDeniedError(ForbiddenError):
    message = _("You don't have access to this dashboard.")
