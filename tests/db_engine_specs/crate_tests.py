from rabbitai.connectors.sqla.models import SqlaTable, TableColumn
from rabbitai.db_engine_specs.crate import CrateEngineSpec
from rabbitai.models.core import Database
from tests.db_engine_specs.base_tests import TestDbEngineSpec


class TestCrateDbEngineSpec(TestDbEngineSpec):
    def test_convert_dttm(self):
        """
        DB Eng Specs (crate): Test conversion to date time
        """
        dttm = self.get_dttm()
        assert CrateEngineSpec.convert_dttm("TIMESTAMP", dttm) == str(
            dttm.timestamp() * 1000
        )

    def test_epoch_to_dttm(self):
        """
        DB Eng Specs (crate): Test epoch to dttm
        """
        assert CrateEngineSpec.epoch_to_dttm() == "{col} * 1000"

    def test_epoch_ms_to_dttm(self):
        """
        DB Eng Specs (crate): Test epoch ms to dttm
        """
        assert CrateEngineSpec.epoch_ms_to_dttm() == "{col}"

    def test_alter_new_orm_column(self):
        """
        DB Eng Specs (crate): Test alter orm column
        """
        database = Database(database_name="crate", sqlalchemy_uri="crate://db")
        tbl = SqlaTable(table_name="druid_tbl", database=database)
        col = TableColumn(column_name="ts", type="TIMESTAMP", table=tbl)
        CrateEngineSpec.alter_new_orm_column(col)
        assert col.python_date_format == "epoch_ms"
