from rabbitai.db_engine_specs.hana import HanaEngineSpec
from tests.integration_tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestHanaDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            HanaEngineSpec.convert_dttm("DATE", dttm),
            "TO_DATE('2019-01-02', 'YYYY-MM-DD')",
        )

        self.assertEqual(
            HanaEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "TO_TIMESTAMP('2019-01-02T03:04:05.678900', 'YYYY-MM-DD\"T\"HH24:MI:SS.ff6')",
        )
