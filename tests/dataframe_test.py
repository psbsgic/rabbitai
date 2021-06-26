# isort:skip_file
import numpy as np
import pandas as pd

import tests.test_app
from rabbitai.dataframe import df_to_records
from rabbitai.db_engine_specs import BaseEngineSpec
from rabbitai.result_set import RabbitaiResultSet

from .base_tests import RabbitaiTestCase


class TestRabbitaiDataFrame(RabbitaiTestCase):
    def test_df_to_records(self):
        data = [("a1", "b1", "c1"), ("a2", "b2", "c2")]
        cursor_descr = (("a", "string"), ("b", "string"), ("c", "string"))
        results = RabbitaiResultSet(data, cursor_descr, BaseEngineSpec)
        df = results.to_pandas_df()

        self.assertEqual(
            df_to_records(df),
            [{"a": "a1", "b": "b1", "c": "c1"}, {"a": "a2", "b": "b2", "c": "c2"}],
        )

    def test_js_max_int(self):
        data = [(1, 1239162456494753670, "c1"), (2, 100, "c2")]
        cursor_descr = (("a", "int"), ("b", "int"), ("c", "string"))
        results = RabbitaiResultSet(data, cursor_descr, BaseEngineSpec)
        df = results.to_pandas_df()

        self.assertEqual(
            df_to_records(df),
            [
                {"a": 1, "b": "1239162456494753670", "c": "c1"},
                {"a": 2, "b": 100, "c": "c2"},
            ],
        )
