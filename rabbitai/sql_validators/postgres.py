# -*- coding: utf-8 -*-

import re
from typing import List, Optional

from pgsanity.pgsanity import check_string

from rabbitai.models.core import Database
from rabbitai.sql_validators.base import BaseSQLValidator, SQLValidationAnnotation


class PostgreSQLValidator(BaseSQLValidator):
    """Validate SQL queries using the pgsanity module"""

    name = "PostgreSQLValidator"

    @classmethod
    def validate(
        cls, sql: str, schema: Optional[str], database: Database
    ) -> List[SQLValidationAnnotation]:
        annotations: List[SQLValidationAnnotation] = []
        valid, error = check_string(sql, add_semicolon=True)
        if valid:
            return annotations

        match = re.match(r"^line (\d+): (.*)", error)
        line_number = int(match.group(1)) if match else None
        message = match.group(2) if match else error

        annotations.append(
            SQLValidationAnnotation(
                message=message,
                line_number=line_number,
                start_column=None,
                end_column=None,
            )
        )

        return annotations
