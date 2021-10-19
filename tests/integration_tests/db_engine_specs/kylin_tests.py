from rabbitai.db_engine_specs.kylin import KylinEngineSpec
from tests.integration_tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestKylinDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            KylinEngineSpec.convert_dttm("DATE", dttm), "CAST('2019-01-02' AS DATE)"
        )

        self.assertEqual(
            KylinEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "CAST('2019-01-02 03:04:05' AS TIMESTAMP)",
        )
