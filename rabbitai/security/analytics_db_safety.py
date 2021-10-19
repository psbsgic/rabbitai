# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import NoSuchModuleError

from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import RabbitaiSecurityException

# 不安全的 SQLAlchemy 方言列表
BLOCKLIST = {
    # sqlite 创建一个本地数据库，它允许映射服务器文件系统
    "sqlite",
    # shillelagh 允许打开本地文件(如, 'SELECT * FROM "csv:///etc/passwd"')
    "shillelagh",
    "shillelagh+apsw",
}


def check_sqlalchemy_uri(uri: URL) -> None:
    """
    检查指定 SQLAlchemy 数据库连接地址的合法性。

    :param uri: SQLAlchemy 数据库连接地址。
    :return:
    """

    if uri.drivername in BLOCKLIST:
        try:
            dialect = uri.get_dialect().__name__
        except NoSuchModuleError:
            dialect = uri.drivername

        raise RabbitaiSecurityException(
            RabbitaiError(
                error_type=RabbitaiErrorType.DATABASE_SECURITY_ACCESS_ERROR,
                message=_(
                    "%(dialect)s cannot be used as a data source for security reasons.",
                    dialect=dialect,
                ),
                level=ErrorLevel.ERROR,
            )
        )
