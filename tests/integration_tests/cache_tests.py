"""Unit tests for Superset with caching"""
import json

import pytest

from rabbitai import app, db
from rabbitai.extensions import cache_manager
from rabbitai.utils.core import QueryStatus
from tests.integration_tests.fixtures.birth_names_dashboard import (
    load_birth_names_dashboard_with_slices,
)

from .base_tests import SupersetTestCase


class TestCache(SupersetTestCase):
    def setUp(self):
        self.login(username="admin")
        cache_manager.cache.clear()
        cache_manager.data_cache.clear()

    def tearDown(self):
        cache_manager.cache.clear()
        cache_manager.data_cache.clear()

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_no_data_cache(self):
        data_cache_config = app.config["DATA_CACHE_CONFIG"]
        app.config["DATA_CACHE_CONFIG"] = {"CACHE_TYPE": "null"}
        cache_manager.init_app(app)

        slc = self.get_slice("Girls", db.session)
        json_endpoint = "/rabbitai/explore_json/{}/{}/".format(
            slc.datasource_type, slc.datasource_id
        )
        resp = self.get_json_resp(
            json_endpoint, {"form_data": json.dumps(slc.viz.form_data)}
        )
        resp_from_cache = self.get_json_resp(
            json_endpoint, {"form_data": json.dumps(slc.viz.form_data)}
        )
        # restore DATA_CACHE_CONFIG
        app.config["DATA_CACHE_CONFIG"] = data_cache_config
        self.assertFalse(resp["is_cached"])
        self.assertFalse(resp_from_cache["is_cached"])

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_slice_data_cache(self):
        # Override cache config
        data_cache_config = app.config["DATA_CACHE_CONFIG"]
        cache_default_timeout = app.config["CACHE_DEFAULT_TIMEOUT"]
        app.config["CACHE_DEFAULT_TIMEOUT"] = 100
        app.config["DATA_CACHE_CONFIG"] = {
            "CACHE_TYPE": "simple",
            "CACHE_DEFAULT_TIMEOUT": 10,
            "CACHE_KEY_PREFIX": "rabbitai_data_cache",
        }
        cache_manager.init_app(app)

        slc = self.get_slice("Boys", db.session)
        json_endpoint = "/rabbitai/explore_json/{}/{}/".format(
            slc.datasource_type, slc.datasource_id
        )
        resp = self.get_json_resp(
            json_endpoint, {"form_data": json.dumps(slc.viz.form_data)}
        )
        resp_from_cache = self.get_json_resp(
            json_endpoint, {"form_data": json.dumps(slc.viz.form_data)}
        )
        self.assertFalse(resp["is_cached"])
        self.assertTrue(resp_from_cache["is_cached"])
        # should fallback to default cache timeout
        self.assertEqual(resp_from_cache["cache_timeout"], 10)
        self.assertEqual(resp_from_cache["status"], QueryStatus.SUCCESS)
        self.assertEqual(resp["data"], resp_from_cache["data"])
        self.assertEqual(resp["query"], resp_from_cache["query"])
        # should exists in `data_cache`
        self.assertEqual(
            cache_manager.data_cache.get(resp_from_cache["cache_key"])["query"],
            resp_from_cache["query"],
        )
        # should not exists in `cache`
        self.assertIsNone(cache_manager.cache.get(resp_from_cache["cache_key"]))

        # reset cache config
        app.config["DATA_CACHE_CONFIG"] = data_cache_config
        app.config["CACHE_DEFAULT_TIMEOUT"] = cache_default_timeout
        cache_manager.init_app(app)
