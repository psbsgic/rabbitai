from rabbitai.exceptions import RabbitaiException


class DAOException(RabbitaiException):
    """
    DAO 错误基类
    """


class DAOCreateFailedError(DAOException):
    """
    DAO 创建失败错误
    """

    message = "创建失败"


class DAOUpdateFailedError(DAOException):
    """
    DAO 更新失败错误
    """

    message = "更新失败"


class DAODeleteFailedError(DAOException):
    """
    DAO 删除失败错误
    """

    message = "删除失败"


class DAOConfigError(DAOException):
    """
    DAO 缺失配置失败错误
    """

    message = "DAO 配置错误，缺失模型定义"
