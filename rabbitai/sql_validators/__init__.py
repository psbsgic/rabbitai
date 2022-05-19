from typing import Optional, Type

from . import base, postgres, presto_db
from .base import SQLValidationAnnotation


def get_validator_by_name(name: str) -> Optional[Type[base.BaseSQLValidator]]:
    """
    依据指定名称获取SQL验证器。

    :param name: 名称。

    :return:
    """

    return {
        "PrestoDBSQLValidator": presto_db.PrestoDBSQLValidator,
        "PostgreSQLValidator": postgres.PostgreSQLValidator,
    }.get(name)
