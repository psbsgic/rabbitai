from rabbitai.commands.exceptions import CommandException


class IncorrectVersionError(CommandException):
    status = 422
    message = "Import has incorrect version"
