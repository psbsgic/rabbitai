from collections import defaultdict
from typing import Any, Dict, List, Optional

from flask_babel import gettext as _
from marshmallow import ValidationError

from rabbitai.errors import ErrorLevel, RabbitaiError, RabbitaiErrorType


class RabbitaiException(Exception):
    status = 500
    message = ""

    def __init__(
        self, message: str = "", exception: Optional[Exception] = None,
    ) -> None:
        if message:
            self.message = message
        self._exception = exception
        super().__init__(self.message)

    @property
    def exception(self) -> Optional[Exception]:
        return self._exception


class RabbitaiErrorException(RabbitaiException):
    """Exceptions with a single RabbitaiErrorType associated with them"""

    def __init__(self, error: RabbitaiError) -> None:
        super().__init__(error.message)
        self.error = error


class RabbitaiErrorFromParamsException(RabbitaiErrorException):
    """Exceptions that pass in parameters to construct a RabbitaiError"""

    def __init__(
        self,
        error_type: RabbitaiErrorType,
        message: str,
        level: ErrorLevel,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            RabbitaiError(
                error_type=error_type, message=message, level=level, extra=extra or {}
            )
        )


class RabbitaiErrorsException(RabbitaiException):
    """Exceptions with multiple RabbitaiErrorType associated with them"""

    def __init__(self, errors: List[RabbitaiError]) -> None:
        super().__init__(str(errors))
        self.errors = errors


class RabbitaiTimeoutException(RabbitaiErrorFromParamsException):
    status = 408


class RabbitaiGenericDBErrorException(RabbitaiErrorFromParamsException):
    status = 400

    def __init__(
        self,
        message: str,
        level: ErrorLevel = ErrorLevel.ERROR,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            RabbitaiErrorType.GENERIC_DB_ENGINE_ERROR, message, level, extra,
        )


class RabbitaiTemplateParamsErrorException(RabbitaiErrorFromParamsException):
    status = 400

    def __init__(
        self,
        message: str,
        level: ErrorLevel = ErrorLevel.ERROR,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            RabbitaiErrorType.MISSING_TEMPLATE_PARAMS_ERROR, message, level, extra,
        )


class RabbitaiSecurityException(RabbitaiErrorException):
    status = 401

    def __init__(
        self, error: RabbitaiError, payload: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(error)
        self.payload = payload


class RabbitaiVizException(RabbitaiErrorsException):
    status = 400


class NoDataException(RabbitaiException):
    status = 400


class NullValueException(RabbitaiException):
    status = 400


class RabbitaiTemplateException(RabbitaiException):
    pass


class SpatialException(RabbitaiException):
    pass


class CertificateException(RabbitaiException):
    message = _("Invalid certificate")


class DatabaseNotFound(RabbitaiException):
    status = 400


class QueryObjectValidationError(RabbitaiException):
    status = 400


class CacheLoadError(RabbitaiException):
    status = 404


class DashboardImportException(RabbitaiException):
    pass


class SerializationError(RabbitaiException):
    pass


class InvalidPayloadFormatError(RabbitaiErrorException):
    status = 400

    def __init__(self, message: str = "Request payload has incorrect format"):
        error = RabbitaiError(
            message=message,
            error_type=RabbitaiErrorType.INVALID_PAYLOAD_FORMAT_ERROR,
            level=ErrorLevel.ERROR,
            extra={},
        )
        super().__init__(error)


class InvalidPayloadSchemaError(RabbitaiErrorException):
    status = 422

    def __init__(self, error: ValidationError):
        # dataclasses.asdict does not work with defaultdict, convert to dict
        # https://bugs.python.org/issue35540
        for k, v in error.messages.items():
            if isinstance(v, defaultdict):
                error.messages[k] = dict(v)
        error = RabbitaiError(
            message="An error happened when validating the request",
            error_type=RabbitaiErrorType.INVALID_PAYLOAD_SCHEMA_ERROR,
            level=ErrorLevel.ERROR,
            extra={"messages": error.messages},
        )
        super().__init__(error)
