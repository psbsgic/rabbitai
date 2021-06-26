# pylint: disable=too-few-public-methods

from typing import Any, Dict, List, Optional

from rabbitai.models.core import Database


class SQLValidationAnnotation:
    """Represents a single annotation (error/warning) in an SQL querytext"""

    def __init__(
        self,
        message: str,
        line_number: Optional[int],
        start_column: Optional[int],
        end_column: Optional[int],
    ):
        self.message = message
        self.line_number = line_number
        self.start_column = start_column
        self.end_column = end_column

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of this annotation"""
        return {
            "line_number": self.line_number,
            "start_column": self.start_column,
            "end_column": self.end_column,
            "message": self.message,
        }


class BaseSQLValidator:
    """BaseSQLValidator defines the interface for checking that a given sql
    query is valid for a given database engine."""

    name = "BaseSQLValidator"

    @classmethod
    def validate(
        cls, sql: str, schema: Optional[str], database: Database
    ) -> List[SQLValidationAnnotation]:
        """Check that the given SQL querystring is valid for the given engine"""
        raise NotImplementedError
