from flask_babel import lazy_gettext as _
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import NoSuchModuleError

from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType
from rabbitai.exceptions import RabbitaiSecurityException

# list of unsafe SQLAlchemy dialects
BLOCKLIST = {
    # sqlite creates a local DB, which allows mapping server's filesystem
    "sqlite",
    # shillelagh allows opening local files (eg, 'SELECT * FROM "csv:///etc/passwd"')
    "shillelagh",
    "shillelagh+apsw",
}


def check_sqlalchemy_uri(uri: URL) -> None:
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
