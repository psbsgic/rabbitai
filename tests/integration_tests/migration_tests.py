import json

from rabbitai.migrations.versions.fb13d49b72f9_better_filters import (
    Slice,
    upgrade_slice,
)

from .base_tests import SupersetTestCase


class TestMigration(SupersetTestCase):
    def test_upgrade_slice(self):
        slc = Slice(
            slice_name="FOO",
            viz_type="filter_box",
            params=json.dumps(dict(metric="foo", groupby=["bar"])),
        )
        upgrade_slice(slc)
        params = json.loads(slc.params)
        self.assertNotIn("metric", params)
        self.assertIn("filter_configs", params)

        cfg = params["filter_configs"][0]
        self.assertEqual(cfg.get("metric"), "foo")
