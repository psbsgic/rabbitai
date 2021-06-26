from rabbitai.db_engine_specs.dremio import DremioEngineSpec
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestDremioDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            DremioEngineSpec.convert_dttm("DATE", dttm),
            "TO_DATE('2019-01-02', 'YYYY-MM-DD')",
        )

        self.assertEqual(
            DremioEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "TO_TIMESTAMP('2019-01-02 03:04:05.678', 'YYYY-MM-DD HH24:MI:SS.FFF')",
        )
