# isort:skip_file
"""Unit tests for Superset cache warmup"""
import datetime
import json
from unittest.mock import MagicMock
from tests.integration_tests.fixtures.birth_names_dashboard import (
    load_birth_names_dashboard_with_slices,
)

from sqlalchemy import String, Date, Float

import pytest
import pandas as pd

from rabbitai.models.slice import Slice
from rabbitai.utils.core import get_example_database

from rabbitai import db

from rabbitai.models.core import Log
from rabbitai.models.tags import get_tag, ObjectTypes, TaggedObject, TagTypes
from rabbitai.tasks.cache import (
    DashboardTagsStrategy,
    get_form_data,
    TopNDashboardsStrategy,
)

from .base_tests import SupersetTestCase
from .dashboard_utils import create_dashboard, create_slice, create_table_for_dashboard
from .fixtures.unicode_dashboard import load_unicode_dashboard_with_slice

URL_PREFIX = "http://0.0.0.0:8081"

mock_positions = {
    "DASHBOARD_VERSION_KEY": "v2",
    "DASHBOARD_CHART_TYPE-1": {
        "type": "CHART",
        "id": "DASHBOARD_CHART_TYPE-1",
        "children": [],
        "meta": {"width": 4, "height": 50, "chartId": 1},
    },
    "DASHBOARD_CHART_TYPE-2": {
        "type": "CHART",
        "id": "DASHBOARD_CHART_TYPE-2",
        "children": [],
        "meta": {"width": 4, "height": 50, "chartId": 2},
    },
}


class TestCacheWarmUp(SupersetTestCase):
    def test_get_form_data_chart_only(self):
        chart_id = 1
        result = get_form_data(chart_id, None)
        expected = {"slice_id": chart_id}
        self.assertEqual(result, expected)

    def test_get_form_data_no_dashboard_metadata(self):
        chart_id = 1
        dashboard = MagicMock()
        dashboard.json_metadata = None
        dashboard.position_json = json.dumps(mock_positions)
        result = get_form_data(chart_id, dashboard)
        expected = {"slice_id": chart_id}
        self.assertEqual(result, expected)

    def test_get_form_data_immune_slice(self):
        chart_id = 1
        filter_box_id = 2
        dashboard = MagicMock()
        dashboard.position_json = json.dumps(mock_positions)
        dashboard.json_metadata = json.dumps(
            {
                "filter_scopes": {
                    str(filter_box_id): {
                        "name": {"scope": ["ROOT_ID"], "immune": [chart_id]}
                    }
                },
                "default_filters": json.dumps(
                    {str(filter_box_id): {"name": ["Alice", "Bob"]}}
                ),
            }
        )
        result = get_form_data(chart_id, dashboard)
        expected = {"slice_id": chart_id}
        self.assertEqual(result, expected)

    def test_get_form_data_no_default_filters(self):
        chart_id = 1
        dashboard = MagicMock()
        dashboard.json_metadata = json.dumps({})
        dashboard.position_json = json.dumps(mock_positions)
        result = get_form_data(chart_id, dashboard)
        expected = {"slice_id": chart_id}
        self.assertEqual(result, expected)

    def test_get_form_data_immune_fields(self):
        chart_id = 1
        filter_box_id = 2
        dashboard = MagicMock()
        dashboard.position_json = json.dumps(mock_positions)
        dashboard.json_metadata = json.dumps(
            {
                "default_filters": json.dumps(
                    {
                        str(filter_box_id): {
                            "name": ["Alice", "Bob"],
                            "__time_range": "100 years ago : today",
                        }
                    }
                ),
                "filter_scopes": {
                    str(filter_box_id): {
                        "__time_range": {"scope": ["ROOT_ID"], "immune": [chart_id]}
                    }
                },
            }
        )
        result = get_form_data(chart_id, dashboard)
        expected = {
            "slice_id": chart_id,
            "extra_filters": [{"col": "name", "op": "in", "val": ["Alice", "Bob"]}],
        }
        self.assertEqual(result, expected)

    def test_get_form_data_no_extra_filters(self):
        chart_id = 1
        filter_box_id = 2
        dashboard = MagicMock()
        dashboard.position_json = json.dumps(mock_positions)
        dashboard.json_metadata = json.dumps(
            {
                "default_filters": json.dumps(
                    {str(filter_box_id): {"__time_range": "100 years ago : today"}}
                ),
                "filter_scopes": {
                    str(filter_box_id): {
                        "__time_range": {"scope": ["ROOT_ID"], "immune": [chart_id]}
                    }
                },
            }
        )
        result = get_form_data(chart_id, dashboard)
        expected = {"slice_id": chart_id}
        self.assertEqual(result, expected)

    def test_get_form_data(self):
        chart_id = 1
        filter_box_id = 2
        dashboard = MagicMock()
        dashboard.position_json = json.dumps(mock_positions)
        dashboard.json_metadata = json.dumps(
            {
                "default_filters": json.dumps(
                    {
                        str(filter_box_id): {
                            "name": ["Alice", "Bob"],
                            "__time_range": "100 years ago : today",
                        }
                    }
                )
            }
        )
        result = get_form_data(chart_id, dashboard)
        expected = {
            "slice_id": chart_id,
            "extra_filters": [
                {"col": "name", "op": "in", "val": ["Alice", "Bob"]},
                {"col": "__time_range", "op": "==", "val": "100 years ago : today"},
            ],
        }
        self.assertEqual(result, expected)

    @pytest.mark.usefixtures("load_birth_names_dashboard_with_slices")
    def test_top_n_dashboards_strategy(self):
        # create a top visited dashboard
        db.session.query(Log).delete()
        self.login(username="admin")
        dash = self.get_dash_by_slug("births")
        for _ in range(10):
            self.client.get(f"/rabbitai/dashboard/{dash.id}/")

        strategy = TopNDashboardsStrategy(1)
        result = sorted(strategy.get_urls())
        expected = sorted([f"{URL_PREFIX}{slc.url}" for slc in dash.slices])
        self.assertEqual(result, expected)

    def reset_tag(self, tag):
        """Remove associated object from tag, used to reset tests"""
        if tag.objects:
            for o in tag.objects:
                db.session.delete(o)
            db.session.commit()

    @pytest.mark.usefixtures(
        "load_unicode_dashboard_with_slice", "load_birth_names_dashboard_with_slices"
    )
    def test_dashboard_tags(self):
        tag1 = get_tag("tag1", db.session, TagTypes.custom)
        # delete first to make test idempotent
        self.reset_tag(tag1)

        strategy = DashboardTagsStrategy(["tag1"])
        result = sorted(strategy.get_urls())
        expected = []
        self.assertEqual(result, expected)

        # tag dashboard 'births' with `tag1`
        tag1 = get_tag("tag1", db.session, TagTypes.custom)
        dash = self.get_dash_by_slug("births")
        tag1_urls = sorted([f"{URL_PREFIX}{slc.url}" for slc in dash.slices])
        tagged_object = TaggedObject(
            tag_id=tag1.id, object_id=dash.id, object_type=ObjectTypes.dashboard
        )
        db.session.add(tagged_object)
        db.session.commit()

        self.assertEqual(sorted(strategy.get_urls()), tag1_urls)

        strategy = DashboardTagsStrategy(["tag2"])
        tag2 = get_tag("tag2", db.session, TagTypes.custom)
        self.reset_tag(tag2)

        result = sorted(strategy.get_urls())
        expected = []
        self.assertEqual(result, expected)

        # tag first slice
        dash = self.get_dash_by_slug("unicode-test")
        slc = dash.slices[0]
        tag2_urls = [f"{URL_PREFIX}{slc.url}"]
        object_id = slc.id
        tagged_object = TaggedObject(
            tag_id=tag2.id, object_id=object_id, object_type=ObjectTypes.chart
        )
        db.session.add(tagged_object)
        db.session.commit()

        result = sorted(strategy.get_urls())
        self.assertEqual(result, tag2_urls)

        strategy = DashboardTagsStrategy(["tag1", "tag2"])

        result = sorted(strategy.get_urls())
        expected = sorted(tag1_urls + tag2_urls)
        self.assertEqual(result, expected)
