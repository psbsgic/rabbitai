from unittest.mock import MagicMock

from sqlalchemy import column

from rabbitai.db_engine_specs.elasticsearch import (
    ElasticSearchEngineSpec,
    OpenDistroEngineSpec,
)
from tests.integration_tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestElasticSearchDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            ElasticSearchEngineSpec.convert_dttm("DATETIME", dttm),
            "CAST('2019-01-02T03:04:05' AS DATETIME)",
        )

    def test_opendistro_convert_dttm(self):
        """
        DB Eng Specs (opendistro): Test convert_dttm
        """
        dttm = self.get_dttm()

        self.assertEqual(
            OpenDistroEngineSpec.convert_dttm("DATETIME", dttm),
            "'2019-01-02T03:04:05'",
        )

    def test_opendistro_sqla_column_label(self):
        """
        DB Eng Specs (opendistro): Test column label
        """
        test_cases = {
            "Col": "Col",
            "Col.keyword": "Col_keyword",
        }
        for original, expected in test_cases.items():
            actual = OpenDistroEngineSpec.make_label_compatible(column(original).name)
            self.assertEqual(actual, expected)

    def test_opendistro_strip_comments(self):
        """
        DB Eng Specs (opendistro): Test execute sql strip comments
        """
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = []

        OpenDistroEngineSpec.execute(
            mock_cursor, "-- some comment \nSELECT 1\n --other comment"
        )
        mock_cursor.execute.assert_called_once_with("SELECT 1\n")
