from unittest import mock

import pytest

from rabbitai.db_engine_specs.clickhouse import ClickHouseEngineSpec
from rabbitai.db_engine_specs.exceptions import RabbitaiDBAPIDatabaseError
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestClickHouseDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        dttm = self.get_dttm()

        self.assertEqual(
            ClickHouseEngineSpec.convert_dttm("DATE", dttm), "toDate('2019-01-02')"
        )

        self.assertEqual(
            ClickHouseEngineSpec.convert_dttm("DATETIME", dttm),
            "toDateTime('2019-01-02 03:04:05')",
        )

    def test_execute_connection_error(self):
        from urllib3.exceptions import NewConnectionError

        cursor = mock.Mock()
        cursor.execute.side_effect = NewConnectionError(
            "Dummypool", message="Exception with sensitive data"
        )
        with pytest.raises(RabbitaiDBAPIDatabaseError) as ex:
            ClickHouseEngineSpec.execute(cursor, "SELECT col1 from table1")
