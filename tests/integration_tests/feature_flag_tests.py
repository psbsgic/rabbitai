from unittest.mock import patch

from rabbitai import is_feature_enabled
from tests.integration_tests.base_tests import SupersetTestCase


class TestFeatureFlag(SupersetTestCase):
    @patch.dict(
        "rabbitai.extensions.feature_flag_manager._feature_flags",
        {"FOO": True},
        clear=True,
    )
    def test_existing_feature_flags(self):
        self.assertTrue(is_feature_enabled("FOO"))

    @patch.dict(
        "rabbitai.extensions.feature_flag_manager._feature_flags", {}, clear=True
    )
    def test_nonexistent_feature_flags(self):
        self.assertFalse(is_feature_enabled("FOO"))

    def test_feature_flags(self):
        self.assertEqual(is_feature_enabled("foo"), "bar")
        self.assertEqual(is_feature_enabled("super"), "set")
