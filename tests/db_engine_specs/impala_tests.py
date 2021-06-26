from rabbitai.db_engine_specs.impala import ImpalaEngineSpec
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestImpalaDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            ImpalaEngineSpec.convert_dttm("DATE", dttm), "CAST('2019-01-02' AS DATE)"
        )

        self.assertEqual(
            ImpalaEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "CAST('2019-01-02T03:04:05.678900' AS TIMESTAMP)",
        )
