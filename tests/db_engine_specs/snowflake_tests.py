import json

from rabbitai.db_engine_specs.snowflake import SnowflakeEngineSpec
from rabbitai.models.core import Database
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestSnowflakeDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        test_cases = {
            "DATE": "TO_DATE('2019-01-02')",
            "DATETIME": "CAST('2019-01-02T03:04:05.678900' AS DATETIME)",
            "TIMESTAMP": "TO_TIMESTAMP('2019-01-02T03:04:05.678900')",
        }

        for type_, expected in test_cases.items():
            self.assertEqual(SnowflakeEngineSpec.convert_dttm(type_, dttm), expected)

    def test_database_connection_test_mutator(self):
        database = Database(sqlalchemy_uri="snowflake://abc")
        SnowflakeEngineSpec.mutate_db_for_connection_test(database)
        engine_params = json.loads(database.extra or "{}")

        self.assertDictEqual(
            {"engine_params": {"connect_args": {"validate_default_parameters": True}}},
            engine_params,
        )
