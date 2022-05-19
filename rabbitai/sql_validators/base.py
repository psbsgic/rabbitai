# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from rabbitai.models.core import Database


class SQLValidationAnnotation:
    """表示SQL查询文本中的单个注释（错误/警告），包括：message、line_number、start_column、end_column"""

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
        """返回此注释的字典表示形式"""
        return {
            "line_number": self.line_number,
            "start_column": self.start_column,
            "end_column": self.end_column,
            "message": self.message,
        }


class BaseSQLValidator:
    """
    基础SQL验证器，该类定义用于检查给定sql查询对于特定数据库引擎是否有效的接口。

    """

    name = "BaseSQLValidator"

    @classmethod
    def validate(
        cls, sql: str, schema: Optional[str], database: Database
    ) -> List[SQLValidationAnnotation]:
        """
        检查给定的SQL查询字符串是否对给定引擎有效。

        :param sql: SQL查询字符串。
        :param schema: 模式。
        :param database: 数据库对象模型。
        :return:
        """

        raise NotImplementedError
