from unittest import mock

from sqlalchemy import column

from rabbitai.db_engine_specs.druid import DruidEngineSpec
from tests.db_engine_specs.base_tests import TestDbEngineSpec
from tests.fixtures.certificates import ssl_certificate
from tests.fixtures.database import default_db_extra


class TestDruidDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            DruidEngineSpec.convert_dttm("DATETIME", dttm),
            "TIME_PARSE('2019-01-02T03:04:05')",
        )

        self.assertEqual(
            DruidEngineSpec.convert_dttm("TIMESTAMP", dttm),
            "TIME_PARSE('2019-01-02T03:04:05')",
        )

        self.assertEqual(
            DruidEngineSpec.convert_dttm("DATE", dttm),
            "CAST(TIME_PARSE('2019-01-02') AS DATE)",
        )

    def test_timegrain_expressions(self):
        """
        DB Eng Specs (druid): Test time grain expressions
        """
        col = "__time"
        sqla_col = column(col)
        test_cases = {
            "PT1S": f"FLOOR({col} TO SECOND)",
            "PT5M": f"TIME_FLOOR({col}, 'PT5M')",
        }
        for grain, expected in test_cases.items():
            actual = DruidEngineSpec.get_timestamp_expr(
                col=sqla_col, pdf=None, time_grain=grain
            )
            self.assertEqual(str(actual), expected)

    def test_extras_without_ssl(self):
        db = mock.Mock()
        db.extra = default_db_extra
        db.server_cert = None
        extras = DruidEngineSpec.get_extra_params(db)
        assert "connect_args" not in extras["engine_params"]

    def test_extras_with_ssl(self):
        db = mock.Mock()
        db.extra = default_db_extra
        db.server_cert = ssl_certificate
        extras = DruidEngineSpec.get_extra_params(db)
        connect_args = extras["engine_params"]["connect_args"]
        assert connect_args["scheme"] == "https"
        assert "ssl_verify_cert" in connect_args
