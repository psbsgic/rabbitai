from rabbitai.db_engine_specs.gsheets import GSheetsEngineSpec
from rabbitai.errors import ErrorLevel, SupersetError, SupersetErrorType
from tests.integration_tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestGsheetsDbEngineSpec(TestDbEngineSpec):
    def test_extract_errors(self):
        """
        Test that custom error messages are extracted correctly.
        """
        msg = 'SQLError: near "fromm": syntax error'
        result = GSheetsEngineSpec.extract_errors(Exception(msg))
        assert result == [
            SupersetError(
                message='Please check your query for syntax errors near "fromm". Then, try running your query again.',
                error_type=SupersetErrorType.SYNTAX_ERROR,
                level=ErrorLevel.ERROR,
                extra={
                    "engine_name": "Google Sheets",
                    "issue_codes": [
                        {
                            "code": 1030,
                            "message": "Issue 1030 - The query has a syntax error.",
                        }
                    ],
                },
            )
        ]
