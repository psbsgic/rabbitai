# isort:skip_file
"""Unit tests for Rabbitai"""
from typing import Any, Dict, Tuple

from marshmallow import ValidationError
from tests.test_app import app
from rabbitai.charts.schemas import ChartDataQueryContextSchema
from rabbitai.common.query_context import QueryContext
from tests.base_tests import RabbitaiTestCase
from tests.fixtures.query_context import get_query_context


class TestSchema(RabbitaiTestCase):
    def test_query_context_limit_and_offset(self):
        self.login(username="admin")
        payload = get_query_context("birth_names")

        # Use defaults
        payload["queries"][0].pop("row_limit", None)
        payload["queries"][0].pop("row_offset", None)
        query_context = ChartDataQueryContextSchema().load(payload)
        query_object = query_context.queries[0]
        self.assertEqual(query_object.row_limit, app.config["ROW_LIMIT"])
        self.assertEqual(query_object.row_offset, 0)

        # Valid limit and offset
        payload["queries"][0]["row_limit"] = 100
        payload["queries"][0]["row_offset"] = 200
        query_context = ChartDataQueryContextSchema().load(payload)
        query_object = query_context.queries[0]
        self.assertEqual(query_object.row_limit, 100)
        self.assertEqual(query_object.row_offset, 200)

        # too low limit and offset
        payload["queries"][0]["row_limit"] = -1
        payload["queries"][0]["row_offset"] = -1
        with self.assertRaises(ValidationError) as context:
            _ = ChartDataQueryContextSchema().load(payload)
        self.assertIn("row_limit", context.exception.messages["queries"][0])
        self.assertIn("row_offset", context.exception.messages["queries"][0])

    def test_query_context_null_timegrain(self):
        self.login(username="admin")
        payload = get_query_context("birth_names")
        payload["queries"][0]["extras"]["time_grain_sqla"] = None
        _ = ChartDataQueryContextSchema().load(payload)

    def test_query_context_series_limit(self):
        self.login(username="admin")
        payload = get_query_context("birth_names")

        payload["queries"][0]["timeseries_limit"] = 2
        payload["queries"][0]["timeseries_limit_metric"] = {
            "expressionType": "SIMPLE",
            "column": {
                "id": 334,
                "column_name": "gender",
                "filterable": True,
                "groupby": True,
                "is_dttm": False,
                "type": "VARCHAR(16)",
                "optionName": "_col_gender",
            },
            "aggregate": "COUNT_DISTINCT",
            "label": "COUNT_DISTINCT(gender)",
        }
        _ = ChartDataQueryContextSchema().load(payload)

    def test_query_context_null_post_processing_op(self):
        self.login(username="admin")
        payload = get_query_context("birth_names")

        payload["queries"][0]["post_processing"] = [None]
        query_context = ChartDataQueryContextSchema().load(payload)
        self.assertEqual(query_context.queries[0].post_processing, [])
