from rabbitai.exceptions import RabbitaiException


class RabbitaiDBAPIError(RabbitaiException):
    pass


class RabbitaiDBAPIDataError(RabbitaiDBAPIError):
    pass


class RabbitaiDBAPIDatabaseError(RabbitaiDBAPIError):
    pass


class RabbitaiDBAPIDisconnectionError(RabbitaiDBAPIError):
    pass


class RabbitaiDBAPIOperationalError(RabbitaiDBAPIError):
    pass


class RabbitaiDBAPIProgrammingError(RabbitaiDBAPIError):
    pass
