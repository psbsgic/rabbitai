"""Unit tests for Superset"""
import json
from contextlib import contextmanager
from unittest import mock

import pytest

from rabbitai import app, ConnectorRegistry, db
from rabbitai.connectors.sqla.models import SqlaTable
from rabbitai.datasets.commands.exceptions import DatasetNotFoundError
from rabbitai.exceptions import SupersetGenericDBErrorException
from rabbitai.models.core import Database
from rabbitai.utils.core import get_example_database
from tests.integration_tests.base_tests import db_insert_temp_object, SupersetTestCase
from tests.integration_tests.fixtures.birth_names_dashboard import (
    load_birth_names_dashboard_with_slices,
)
from tests.integration_tests.fixtures.datasource import get_datasource_post


@contextmanager
def create_test_table_context(database: Database):
    database.get_sqla_engine().execute(
        "CREATE TABLE test_table AS SELECT 1 as first, 2 as second"
    )
    database.get_sqla_engine().execute(
        "INSERT INTO test_table (first, second) VALUES (1, 2)"
    )
    database.get_sqla_engine().execute(
        "INSERT INTO test_table (first, second) VALUES (3, 4)"
    )

    yield db.session
    database.get_sqla_engine().execute("DROP TABLE test_table")


class TestDatasource(SupersetTestCase):
    def setUp(self):
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_external_metadata_for_physical_table(self):
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")
        url = f"/datasource/external_metadata/table/{tbl.id}/"
        resp = self.get_json_resp(url)
        col_names = {o.get("name") for o in resp}
        self.assertEqual(
            col_names, {"num_boys", "num", "gender", "name", "ds", "state", "num_girls"}
        )

    def test_external_metadata_for_virtual_table(self):
        self.login(username="admin")
        session = db.session
        table = SqlaTable(
            table_name="dummy_sql_table",
            database=get_example_database(),
            sql="select 123 as intcol, 'abc' as strcol",
        )
        session.add(table)
        session.commit()

        table = self.get_table(name="dummy_sql_table")
        url = f"/datasource/external_metadata/table/{table.id}/"
        resp = self.get_json_resp(url)
        assert {o.get("name") for o in resp} == {"intcol", "strcol"}
        session.delete(table)
        session.commit()

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_external_metadata_by_name_for_physical_table(self):
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")
        # empty schema need to be represented by undefined
        url = (
            f"/datasource/external_metadata_by_name/table/"
            f"{tbl.database.database_name}/undefined/{tbl.table_name}/"
        )
        resp = self.get_json_resp(url)
        col_names = {o.get("name") for o in resp}
        self.assertEqual(
            col_names, {"num_boys", "num", "gender", "name", "ds", "state", "num_girls"}
        )

    def test_external_metadata_by_name_for_virtual_table(self):
        self.login(username="admin")
        session = db.session
        table = SqlaTable(
            table_name="dummy_sql_table",
            database=get_example_database(),
            sql="select 123 as intcol, 'abc' as strcol",
        )
        session.add(table)
        session.commit()

        table = self.get_table(name="dummy_sql_table")
        # empty schema need to be represented by undefined
        url = (
            f"/datasource/external_metadata_by_name/table/"
            f"{table.database.database_name}/undefined/{table.table_name}/"
        )
        resp = self.get_json_resp(url)
        assert {o.get("name") for o in resp} == {"intcol", "strcol"}
        session.delete(table)
        session.commit()

    def test_external_metadata_by_name_from_sqla_inspector(self):
        self.login(username="admin")
        example_database = get_example_database()
        with create_test_table_context(example_database):
            url = (
                f"/datasource/external_metadata_by_name/table/"
                f"{example_database.database_name}/undefined/test_table/"
            )
            resp = self.get_json_resp(url)
            col_names = {o.get("name") for o in resp}
            self.assertEqual(col_names, {"first", "second"})

        url = (
            f"/datasource/external_metadata_by_name/table/" f"foobar/undefined/foobar/"
        )
        resp = self.get_json_resp(url, raise_on_error=False)
        self.assertIn("error", resp)

    def test_external_metadata_for_virtual_table_template_params(self):
        self.login(username="admin")
        session = db.session
        table = SqlaTable(
            table_name="dummy_sql_table_with_template_params",
            database=get_example_database(),
            sql="select {{ foo }} as intcol",
            template_params=json.dumps({"foo": "123"}),
        )
        session.add(table)
        session.commit()

        table = self.get_table(name="dummy_sql_table_with_template_params")
        url = f"/datasource/external_metadata/table/{table.id}/"
        resp = self.get_json_resp(url)
        assert {o.get("name") for o in resp} == {"intcol"}
        session.delete(table)
        session.commit()

    def test_external_metadata_for_malicious_virtual_table(self):
        self.login(username="admin")
        table = SqlaTable(
            table_name="malicious_sql_table",
            database=get_example_database(),
            sql="delete table birth_names",
        )
        with db_insert_temp_object(table):
            url = f"/datasource/external_metadata/table/{table.id}/"
            resp = self.get_json_resp(url)
            self.assertEqual(resp["error"], "Only `SELECT` statements are allowed")

    def test_external_metadata_for_mutistatement_virtual_table(self):
        self.login(username="admin")
        table = SqlaTable(
            table_name="multistatement_sql_table",
            database=get_example_database(),
            sql="select 123 as intcol, 'abc' as strcol;"
            "select 123 as intcol, 'abc' as strcol",
        )
        with db_insert_temp_object(table):
            url = f"/datasource/external_metadata/table/{table.id}/"
            resp = self.get_json_resp(url)
            self.assertEqual(resp["error"], "Only single queries supported")

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    @mock.patch("rabbitai.connectors.sqla.models.SqlaTable.external_metadata")
    def test_external_metadata_error_return_400(self, mock_get_datasource):
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")
        url = f"/datasource/external_metadata/table/{tbl.id}/"

        mock_get_datasource.side_effect = SupersetGenericDBErrorException("oops")

        pytest.raises(
            SupersetGenericDBErrorException,
            lambda: ConnectorRegistry.get_datasource(
                "table", tbl.id, db.session
            ).external_metadata(),
        )

        resp = self.client.get(url)
        assert resp.status_code == 400

    def compare_lists(self, l1, l2, key):
        l2_lookup = {o.get(key): o for o in l2}
        for obj1 in l1:
            obj2 = l2_lookup.get(obj1.get(key))
            for k in obj1:
                if k not in "id" and obj1.get(k):
                    self.assertEqual(obj1.get(k), obj2.get(k))

    def test_save(self):
        self.login(username="admin")
        tbl_id = self.get_table(name="birth_names").id

        datasource_post = get_datasource_post()
        datasource_post["id"] = tbl_id
        data = dict(data=json.dumps(datasource_post))
        resp = self.get_json_resp("/datasource/save/", data)
        for k in datasource_post:
            if k == "columns":
                self.compare_lists(datasource_post[k], resp[k], "column_name")
            elif k == "metrics":
                self.compare_lists(datasource_post[k], resp[k], "metric_name")
            elif k == "database":
                self.assertEqual(resp[k]["id"], datasource_post[k]["id"])
            else:
                self.assertEqual(resp[k], datasource_post[k])

    def save_datasource_from_dict(self, datasource_post):
        data = dict(data=json.dumps(datasource_post))
        resp = self.get_json_resp("/datasource/save/", data)
        return resp

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_change_database(self):
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")
        tbl_id = tbl.id
        db_id = tbl.database_id
        datasource_post = get_datasource_post()
        datasource_post["id"] = tbl_id

        new_db = self.create_fake_db()
        datasource_post["database"]["id"] = new_db.id
        resp = self.save_datasource_from_dict(datasource_post)
        self.assertEqual(resp["database"]["id"], new_db.id)

        datasource_post["database"]["id"] = db_id
        resp = self.save_datasource_from_dict(datasource_post)
        self.assertEqual(resp["database"]["id"], db_id)

        self.delete_fake_db()

    def test_save_duplicate_key(self):
        self.login(username="admin")
        tbl_id = self.get_table(name="birth_names").id

        datasource_post = get_datasource_post()
        datasource_post["id"] = tbl_id
        datasource_post["columns"].extend(
            [
                {
                    "column_name": "<new column>",
                    "filterable": True,
                    "groupby": True,
                    "expression": "<enter SQL expression here>",
                    "id": "somerandomid",
                },
                {
                    "column_name": "<new column>",
                    "filterable": True,
                    "groupby": True,
                    "expression": "<enter SQL expression here>",
                    "id": "somerandomid2",
                },
            ]
        )
        data = dict(data=json.dumps(datasource_post))
        resp = self.get_json_resp("/datasource/save/", data, raise_on_error=False)
        self.assertIn("Duplicate column name(s): <new column>", resp["error"])

    def test_get_datasource(self):
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")

        datasource_post = get_datasource_post()
        datasource_post["id"] = tbl.id
        data = dict(data=json.dumps(datasource_post))
        self.get_json_resp("/datasource/save/", data)
        url = f"/datasource/get/{tbl.type}/{tbl.id}/"
        resp = self.get_json_resp(url)
        self.assertEqual(resp.get("type"), "table")
        col_names = {o.get("column_name") for o in resp["columns"]}
        self.assertEqual(
            col_names,
            {
                "num_boys",
                "num",
                "gender",
                "name",
                "ds",
                "state",
                "num_girls",
                "num_california",
            },
        )

    def test_get_datasource_with_health_check(self):
        def my_check(datasource):
            return "Warning message!"

        app.config["DATASET_HEALTH_CHECK"] = my_check
        self.login(username="admin")
        tbl = self.get_table(name="birth_names")
        datasource = ConnectorRegistry.get_datasource("table", tbl.id, db.session)
        assert datasource.health_check_message == "Warning message!"
        app.config["DATASET_HEALTH_CHECK"] = None

    def test_get_datasource_failed(self):
        pytest.raises(
            DatasetNotFoundError,
            lambda: ConnectorRegistry.get_datasource("table", 9999999, db.session),
        )

        self.login(username="admin")
        resp = self.get_json_resp("/datasource/get/druid/500000/", raise_on_error=False)
        self.assertEqual(resp.get("error"), "Dataset does not exist")

        resp = self.get_json_resp(
            "/datasource/get/invalid-datasource-type/500000/", raise_on_error=False
        )
        self.assertEqual(resp.get("error"), "Dataset does not exist")