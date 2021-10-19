from rabbitai.commands.exceptions import CommandException


class IncorrectVersionError(CommandException):
    status = 422
    message = "Import has incorrect version"


class NoValidFilesFoundError(CommandException):
    status = 400
    message = "No valid import files were found"
