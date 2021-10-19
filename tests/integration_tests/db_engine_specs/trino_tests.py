from sqlalchemy.engine.url import URL

from rabbitai.db_engine_specs.trino import TrinoEngineSpec
from tests.integration_tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestTrinoDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            TrinoEngineSpec.convert_dttm("DATE", dttm),
            "from_iso8601_date('2019-01-02')",
        )

        self.assertEqual(
            TrinoEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "from_iso8601_timestamp('2019-01-02T03:04:05.678900')",
        )

    def test_adjust_database_uri(self):
        url = URL(drivername="trino", database="hive")
        TrinoEngineSpec.adjust_database_uri(url, selected_schema="foobar")
        self.assertEqual(url.database, "hive/foobar")

    def test_adjust_database_uri_when_database_contain_schema(self):
        url = URL(drivername="trino", database="hive/default")
        TrinoEngineSpec.adjust_database_uri(url, selected_schema="foobar")
        self.assertEqual(url.database, "hive/foobar")

    def test_adjust_database_uri_when_selected_schema_is_none(self):
        url = URL(drivername="trino", database="hive")
        TrinoEngineSpec.adjust_database_uri(url, selected_schema=None)
        self.assertEqual(url.database, "hive")

        url.database = "hive/default"
        TrinoEngineSpec.adjust_database_uri(url, selected_schema=None)
        self.assertEqual(url.database, "hive/default")
