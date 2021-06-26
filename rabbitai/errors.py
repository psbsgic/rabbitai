from dataclasses import dataclass  # pylint: disable=wrong-import-order
from enum import Enum
from typing import Any, Dict, Optional

from flask_babel import gettext as _


class RabbitaiErrorType(str, Enum):
    """
    Types of errors that can exist within Rabbitai.

    Keep in sync with rabbitai-frontend/src/components/ErrorMessage/types.ts
    and docs/src/pages/docs/Miscellaneous/issue_codes.mdx
    """

    # Frontend errors
    FRONTEND_CSRF_ERROR = "FRONTEND_CSRF_ERROR"
    FRONTEND_NETWORK_ERROR = "FRONTEND_NETWORK_ERROR"
    FRONTEND_TIMEOUT_ERROR = "FRONTEND_TIMEOUT_ERROR"

    # DB Engine errors
    GENERIC_DB_ENGINE_ERROR = "GENERIC_DB_ENGINE_ERROR"
    COLUMN_DOES_NOT_EXIST_ERROR = "COLUMN_DOES_NOT_EXIST_ERROR"
    TABLE_DOES_NOT_EXIST_ERROR = "TABLE_DOES_NOT_EXIST_ERROR"
    SCHEMA_DOES_NOT_EXIST_ERROR = "SCHEMA_DOES_NOT_EXIST_ERROR"
    CONNECTION_INVALID_USERNAME_ERROR = "CONNECTION_INVALID_USERNAME_ERROR"
    CONNECTION_INVALID_PASSWORD_ERROR = "CONNECTION_INVALID_PASSWORD_ERROR"
    CONNECTION_INVALID_HOSTNAME_ERROR = "CONNECTION_INVALID_HOSTNAME_ERROR"
    CONNECTION_PORT_CLOSED_ERROR = "CONNECTION_PORT_CLOSED_ERROR"
    CONNECTION_HOST_DOWN_ERROR = "CONNECTION_HOST_DOWN_ERROR"
    CONNECTION_ACCESS_DENIED_ERROR = "CONNECTION_ACCESS_DENIED_ERROR"
    CONNECTION_UNKNOWN_DATABASE_ERROR = "CONNECTION_UNKNOWN_DATABASE_ERROR"
    CONNECTION_DATABASE_PERMISSIONS_ERROR = "CONNECTION_DATABASE_PERMISSIONS_ERROR"
    CONNECTION_MISSING_PARAMETERS_ERROR = "CONNECTION_MISSING_PARAMETERS_ERROR"

    # Viz errors
    VIZ_GET_DF_ERROR = "VIZ_GET_DF_ERROR"
    UNKNOWN_DATASOURCE_TYPE_ERROR = "UNKNOWN_DATASOURCE_TYPE_ERROR"
    FAILED_FETCHING_DATASOURCE_INFO_ERROR = "FAILED_FETCHING_DATASOURCE_INFO_ERROR"

    # Security access errors
    TABLE_SECURITY_ACCESS_ERROR = "TABLE_SECURITY_ACCESS_ERROR"
    DATASOURCE_SECURITY_ACCESS_ERROR = "DATASOURCE_SECURITY_ACCESS_ERROR"
    DATABASE_SECURITY_ACCESS_ERROR = "DATABASE_SECURITY_ACCESS_ERROR"
    MISSING_OWNERSHIP_ERROR = "MISSING_OWNERSHIP_ERROR"

    # Other errors
    BACKEND_TIMEOUT_ERROR = "BACKEND_TIMEOUT_ERROR"

    # Sql Lab errors
    MISSING_TEMPLATE_PARAMS_ERROR = "MISSING_TEMPLATE_PARAMS_ERROR"

    # Generic errors
    GENERIC_COMMAND_ERROR = "GENERIC_COMMAND_ERROR"
    GENERIC_BACKEND_ERROR = "GENERIC_BACKEND_ERROR"

    # API errors
    INVALID_PAYLOAD_FORMAT_ERROR = "INVALID_PAYLOAD_FORMAT_ERROR"
    INVALID_PAYLOAD_SCHEMA_ERROR = "INVALID_PAYLOAD_SCHEMA_ERROR"


ERROR_TYPES_TO_ISSUE_CODES_MAPPING = {
    RabbitaiErrorType.BACKEND_TIMEOUT_ERROR: [
        {
            "code": 1000,
            "message": _("Issue 1000 - The datasource is too large to query."),
        },
        {
            "code": 1001,
            "message": _("Issue 1001 - The database is under an unusual load."),
        },
    ],
    RabbitaiErrorType.GENERIC_DB_ENGINE_ERROR: [
        {
            "code": 1002,
            "message": _("Issue 1002 - The database returned an unexpected error."),
        }
    ],
    RabbitaiErrorType.COLUMN_DOES_NOT_EXIST_ERROR: [
        {
            "code": 1003,
            "message": _(
                "Issue 1003 - There is a syntax error in the SQL query. "
                "Perhaps there was a misspelling or a typo."
            ),
        },
        {
            "code": 1004,
            "message": _(
                "Issue 1004 - The column was deleted or renamed in the database."
            ),
        },
    ],
    RabbitaiErrorType.TABLE_DOES_NOT_EXIST_ERROR: [
        {
            "code": 1003,
            "message": _(
                "Issue 1003 - There is a syntax error in the SQL query. "
                "Perhaps there was a misspelling or a typo."
            ),
        },
        {
            "code": 1005,
            "message": _(
                "Issue 1005 - The table was deleted or renamed in the database."
            ),
        },
    ],
    RabbitaiErrorType.SCHEMA_DOES_NOT_EXIST_ERROR: [
        {
            "code": 1003,
            "message": _(
                "Issue 1003 - There is a syntax error in the SQL query. "
                "Perhaps there was a misspelling or a typo."
            ),
        },
        {
            "code": 1016,
            "message": _(
                "Issue 1005 - The schema was deleted or renamed in the database."
            ),
        },
    ],
    RabbitaiErrorType.MISSING_TEMPLATE_PARAMS_ERROR: [
        {
            "code": 1006,
            "message": _(
                "Issue 1006 - One or more parameters specified in the query are "
                "missing."
            ),
        },
    ],
    RabbitaiErrorType.CONNECTION_INVALID_HOSTNAME_ERROR: [
        {
            "code": 1007,
            "message": _("Issue 1007 - The hostname provided can't be resolved."),
        },
    ],
    RabbitaiErrorType.CONNECTION_PORT_CLOSED_ERROR: [
        {"code": 1008, "message": _("Issue 1008 - The port is closed.")},
    ],
    RabbitaiErrorType.CONNECTION_HOST_DOWN_ERROR: [
        {
            "code": 1009,
            "message": _(
                "Issue 1009 - The host might be down, and can't be reached on the "
                "provided port."
            ),
        },
    ],
    RabbitaiErrorType.GENERIC_COMMAND_ERROR: [
        {
            "code": 1010,
            "message": _(
                "Issue 1010 - Rabbitai encountered an error while running a command."
            ),
        },
    ],
    RabbitaiErrorType.GENERIC_BACKEND_ERROR: [
        {
            "code": 1011,
            "message": _("Issue 1011 - Rabbitai encountered an unexpected error."),
        },
    ],
    RabbitaiErrorType.CONNECTION_INVALID_USERNAME_ERROR: [
        {
            "code": 1012,
            "message": _(
                "Issue 1012 - The username provided when "
                "connecting to a database is not valid."
            ),
        },
    ],
    RabbitaiErrorType.CONNECTION_INVALID_PASSWORD_ERROR: [
        {
            "code": 1013,
            "message": _(
                "Issue 1013 - The password provided when "
                "connecting to a database is not valid."
            ),
        },
    ],
    RabbitaiErrorType.CONNECTION_ACCESS_DENIED_ERROR: [
        {
            "code": 1014,
            "message": _("Issue 1014 - Either the username or the password is wrong."),
        },
        {
            "code": 1015,
            "message": _(
                "Issue 1015 - Either the database is "
                "spelled incorrectly or does not exist."
            ),
        },
    ],
    RabbitaiErrorType.CONNECTION_UNKNOWN_DATABASE_ERROR: [
        {
            "code": 1015,
            "message": _(
                "Issue 1015 - Either the database is "
                "spelled incorrectly or does not exist."
            ),
        }
    ],
    RabbitaiErrorType.CONNECTION_DATABASE_PERMISSIONS_ERROR: [
        {
            "code": 1017,
            "message": _("Issue 1017 - User doesn't have the proper permissions."),
        },
    ],
    RabbitaiErrorType.CONNECTION_MISSING_PARAMETERS_ERROR: [
        {
            "code": 1018,
            "message": _(
                "Issue 1018 - One or more parameters needed to configure a "
                "database are missing."
            ),
        },
    ],
    RabbitaiErrorType.INVALID_PAYLOAD_FORMAT_ERROR: [
        {
            "code": 1019,
            "message": _(
                "Issue 1019 - The submitted payload has the incorrect format."
            ),
        }
    ],
    RabbitaiErrorType.INVALID_PAYLOAD_SCHEMA_ERROR: [
        {
            "code": 1020,
            "message": _(
                "Issue 1020 - The submitted payload has the incorrect schema."
            ),
        }
    ],
}


class ErrorLevel(str, Enum):
    """
    Levels of errors that can exist within Rabbitai.

    Keep in sync with rabbitai-frontend/src/components/ErrorMessage/types.ts
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class RabbitaiError:
    """
    An error that is returned to a client.
    """

    message: str
    error_type: RabbitaiErrorType
    level: ErrorLevel
    extra: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """
        Mutates the extra params with user facing error codes that map to backend
        errors.
        """
        issue_codes = ERROR_TYPES_TO_ISSUE_CODES_MAPPING.get(self.error_type)
        if issue_codes:
            self.extra = self.extra or {}
            self.extra.update({"issue_codes": issue_codes})
