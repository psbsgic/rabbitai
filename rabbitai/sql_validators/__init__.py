from typing import Optional, Type

from . import base, postgres, presto_db
from .base import SQLValidationAnnotation


def get_validator_by_name(name: str) -> Optional[Type[base.BaseSQLValidator]]:
    return {
        "PrestoDBSQLValidator": presto_db.PrestoDBSQLValidator,
        "PostgreSQLValidator": postgres.PostgreSQLValidator,
    }.get(name)
