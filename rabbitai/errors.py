# pylint: disable=too-few-public-methods,invalid-name
from dataclasses import dataclass  # pylint: disable=wrong-import-order
from enum import Enum
from typing import Any, Dict, Optional

from flask_babel import gettext as _


class RabbitaiErrorType(str, Enum):
    """
    RabbitAI 中使用的错误类型枚举。

    保持同步于：rabbitai-frontend/src/components/ErrorMessage/types.ts
    和 docs/src/pages/docs/Miscellaneous/issue_codes.mdx
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
    CONNECTION_INVALID_PORT_ERROR = "CONNECTION_INVALID_PORT_ERROR"
    CONNECTION_HOST_DOWN_ERROR = "CONNECTION_HOST_DOWN_ERROR"
    CONNECTION_ACCESS_DENIED_ERROR = "CONNECTION_ACCESS_DENIED_ERROR"
    CONNECTION_UNKNOWN_DATABASE_ERROR = "CONNECTION_UNKNOWN_DATABASE_ERROR"
    CONNECTION_DATABASE_PERMISSIONS_ERROR = "CONNECTION_DATABASE_PERMISSIONS_ERROR"
    CONNECTION_MISSING_PARAMETERS_ERROR = "CONNECTION_MISSING_PARAMETERS_ERROR"
    OBJECT_DOES_NOT_EXIST_ERROR = "OBJECT_DOES_NOT_EXIST_ERROR"
    SYNTAX_ERROR = "SYNTAX_ERROR"

    # Viz errors
    VIZ_GET_DF_ERROR = "VIZ_GET_DF_ERROR"
    UNKNOWN_DATASOURCE_TYPE_ERROR = "UNKNOWN_DATASOURCE_TYPE_ERROR"
    FAILED_FETCHING_DATASOURCE_INFO_ERROR = "FAILED_FETCHING_DATASOURCE_INFO_ERROR"

    # Security access errors
    TABLE_SECURITY_ACCESS_ERROR = "TABLE_SECURITY_ACCESS_ERROR"
    DATASOURCE_SECURITY_ACCESS_ERROR = "DATASOURCE_SECURITY_ACCESS_ERROR"
    DATABASE_SECURITY_ACCESS_ERROR = "DATABASE_SECURITY_ACCESS_ERROR"
    QUERY_SECURITY_ACCESS_ERROR = "QUERY_SECURITY_ACCESS_ERROR"
    MISSING_OWNERSHIP_ERROR = "MISSING_OWNERSHIP_ERROR"

    # Other errors
    BACKEND_TIMEOUT_ERROR = "BACKEND_TIMEOUT_ERROR"
    DATABASE_NOT_FOUND_ERROR = "DATABASE_NOT_FOUND_ERROR"

    # Sql Lab errors
    MISSING_TEMPLATE_PARAMS_ERROR = "MISSING_TEMPLATE_PARAMS_ERROR"
    INVALID_TEMPLATE_PARAMS_ERROR = "INVALID_TEMPLATE_PARAMS_ERROR"
    RESULTS_BACKEND_NOT_CONFIGURED_ERROR = "RESULTS_BACKEND_NOT_CONFIGURED_ERROR"
    DML_NOT_ALLOWED_ERROR = "DML_NOT_ALLOWED_ERROR"
    INVALID_CTAS_QUERY_ERROR = "INVALID_CTAS_QUERY_ERROR"
    INVALID_CVAS_QUERY_ERROR = "INVALID_CVAS_QUERY_ERROR"
    SQLLAB_TIMEOUT_ERROR = "SQLLAB_TIMEOUT_ERROR"
    RESULTS_BACKEND_ERROR = "RESULTS_BACKEND_ERROR"
    ASYNC_WORKERS_ERROR = "ASYNC_WORKERS_ERROR"

    # Generic errors
    GENERIC_COMMAND_ERROR = "GENERIC_COMMAND_ERROR"
    GENERIC_BACKEND_ERROR = "GENERIC_BACKEND_ERROR"

    # API errors
    INVALID_PAYLOAD_FORMAT_ERROR = "INVALID_PAYLOAD_FORMAT_ERROR"
    INVALID_PAYLOAD_SCHEMA_ERROR = "INVALID_PAYLOAD_SCHEMA_ERROR"


ISSUE_CODES = {
    1000: _("The datasource is too large to query."),
    1001: _("The database is under an unusual load."),
    1002: _("The database returned an unexpected error."),
    1003: _(
        "There is a syntax error in the SQL query. "
        "Perhaps there was a misspelling or a typo."
    ),
    1004: _("The column was deleted or renamed in the database."),
    1005: _("The table was deleted or renamed in the database."),
    1006: _("One or more parameters specified in the query are missing."),
    1007: _("The hostname provided can't be resolved."),
    1008: _("The port is closed."),
    1009: _("The host might be down, and can't be reached on the provided port."),
    1010: _("Rabbitai encountered an error while running a command."),
    1011: _("Rabbitai encountered an unexpected error."),
    1012: _("The username provided when connecting to a database is not valid."),
    1013: _("The password provided when connecting to a database is not valid."),
    1014: _("Either the username or the password is wrong."),
    1015: _("Either the database is spelled incorrectly or does not exist."),
    1016: _("The schema was deleted or renamed in the database."),
    1017: _("User doesn't have the proper permissions."),
    1018: _("One or more parameters needed to configure a database are missing."),
    1019: _("The submitted payload has the incorrect format."),
    1020: _("The submitted payload has the incorrect schema."),
    1021: _("Results backend needed for asynchronous queries is not configured."),
    1022: _("Database does not allow data manipulation."),
    1023: _(
        "The CTAS (create table as select) doesn't have a "
        "SELECT statement at the end. Please make sure your query has a "
        "SELECT as its last statement. Then, try running your query again."
    ),
    1024: _("CVAS (create view as select) query has more than one statement."),
    1025: _("CVAS (create view as select) query is not a SELECT statement."),
    1026: _("Query is too complex and takes too long to run."),
    1027: _("The database is currently running too many queries."),
    1028: _("One or more parameters specified in the query are malformatted."),
    1029: _("The object does not exist in the given database."),
    1030: _("The query has a syntax error."),
    1031: _("The results backend no longer has the data from the query."),
    1032: _("The query associated with the results was deleted."),
    1033: _(
        "The results stored in the backend were stored in a "
        "different format, and no longer can be deserialized."
    ),
    1034: _("The port number is invalid."),
    1035: _("Failed to start remote query on a worker."),
    1036: _("The database was deleted."),
}
"""问题代码及其错误信息的字典。"""

ERROR_TYPES_TO_ISSUE_CODES_MAPPING = {
    RabbitaiErrorType.BACKEND_TIMEOUT_ERROR: [1000, 1001],
    RabbitaiErrorType.GENERIC_DB_ENGINE_ERROR: [1002],
    RabbitaiErrorType.COLUMN_DOES_NOT_EXIST_ERROR: [1003, 1004],
    RabbitaiErrorType.TABLE_DOES_NOT_EXIST_ERROR: [1003, 1005],
    RabbitaiErrorType.SCHEMA_DOES_NOT_EXIST_ERROR: [1003, 1016],
    RabbitaiErrorType.MISSING_TEMPLATE_PARAMS_ERROR: [1006],
    RabbitaiErrorType.INVALID_TEMPLATE_PARAMS_ERROR: [1028],
    RabbitaiErrorType.RESULTS_BACKEND_NOT_CONFIGURED_ERROR: [1021],
    RabbitaiErrorType.DML_NOT_ALLOWED_ERROR: [1022],
    RabbitaiErrorType.CONNECTION_INVALID_HOSTNAME_ERROR: [1007],
    RabbitaiErrorType.CONNECTION_PORT_CLOSED_ERROR: [1008],
    RabbitaiErrorType.CONNECTION_HOST_DOWN_ERROR: [1009],
    RabbitaiErrorType.GENERIC_COMMAND_ERROR: [1010],
    RabbitaiErrorType.GENERIC_BACKEND_ERROR: [1011],
    RabbitaiErrorType.CONNECTION_INVALID_USERNAME_ERROR: [1012],
    RabbitaiErrorType.CONNECTION_INVALID_PASSWORD_ERROR: [1013],
    RabbitaiErrorType.CONNECTION_ACCESS_DENIED_ERROR: [1014, 1015],
    RabbitaiErrorType.CONNECTION_UNKNOWN_DATABASE_ERROR: [1015],
    RabbitaiErrorType.CONNECTION_DATABASE_PERMISSIONS_ERROR: [1017],
    RabbitaiErrorType.CONNECTION_MISSING_PARAMETERS_ERROR: [1018],
    RabbitaiErrorType.INVALID_PAYLOAD_FORMAT_ERROR: [1019],
    RabbitaiErrorType.INVALID_PAYLOAD_SCHEMA_ERROR: [1020],
    RabbitaiErrorType.INVALID_CTAS_QUERY_ERROR: [1023],
    RabbitaiErrorType.INVALID_CVAS_QUERY_ERROR: [1024, 1025],
    RabbitaiErrorType.SQLLAB_TIMEOUT_ERROR: [1026, 1027],
    RabbitaiErrorType.OBJECT_DOES_NOT_EXIST_ERROR: [1029],
    RabbitaiErrorType.SYNTAX_ERROR: [1030],
    RabbitaiErrorType.RESULTS_BACKEND_ERROR: [1031, 1032, 1033],
    RabbitaiErrorType.CONNECTION_INVALID_PORT_ERROR: [1034],
    RabbitaiErrorType.ASYNC_WORKERS_ERROR: [1035],
    RabbitaiErrorType.DATABASE_NOT_FOUND_ERROR: [1011, 1036],
}
"""错误类型与问题代码的列表的字典。"""


class ErrorLevel(str, Enum):
    """
    错误级别枚举。

    同步于：rabbitai-frontend/src/components/ErrorMessage/types.ts
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class RabbitaiError:
    """表示返回到客户端的错误，包括属性：message、error_type、level、extra。"""

    message: str
    error_type: RabbitaiErrorType
    level: ErrorLevel
    extra: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """
        使用映射到后端错误的面向用户的错误代码修改额外参数。
        """

        issue_codes = ERROR_TYPES_TO_ISSUE_CODES_MAPPING.get(self.error_type)
        if issue_codes:
            self.extra = self.extra or {}
            self.extra.update(
                {
                    "issue_codes": [
                        {
                            "code": issue_code,
                            "message": (
                                f"Issue {issue_code} - {ISSUE_CODES[issue_code]}"
                            ),
                        }
                        for issue_code in issue_codes
                    ]
                }
            )
