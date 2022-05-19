from rabbitai.commands.exceptions import CommandException


class IncorrectVersionError(CommandException):
    status = 422
    message = "导入版本不正确"


class NoValidFilesFoundError(CommandException):
    status = 400
    message = "找到无效的导入文件"
