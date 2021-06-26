from flask_babel import lazy_gettext as _

from rabbitai.commands.exceptions import CommandException, DeleteFailedError


class CssTemplateBulkDeleteFailedError(DeleteFailedError):
    message = _("CSS template could not be deleted.")


class CssTemplateNotFoundError(CommandException):
    message = _("CSS template not found.")
