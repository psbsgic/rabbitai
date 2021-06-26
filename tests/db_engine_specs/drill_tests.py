from rabbitai.db_engine_specs.drill import DrillEngineSpec
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestDrillDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            DrillEngineSpec.convert_dttm("DATE", dttm),
            "TO_DATE('2019-01-02', 'yyyy-MM-dd')",
        )

        self.assertEqual(
            DrillEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "TO_TIMESTAMP('2019-01-02 03:04:05', 'yyyy-MM-dd HH:mm:ss')",
        )
