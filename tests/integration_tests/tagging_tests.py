from tests.integration_tests.base_tests import SupersetTestCase
from tests.integration_tests.conftest import with_feature_flags


class TestTagging(SupersetTestCase):
    @with_feature_flags(TAGGING_SYSTEM=False)
    def test_tag_view_disabled(self):
        self.login("admin")
        response = self.client.get("/tagview/tags/suggestions/")
        self.assertEqual(404, response.status_code)

    @with_feature_flags(TAGGING_SYSTEM=True)
    def test_tag_view_enabled(self):
        self.login("admin")
        response = self.client.get("/tagview/tags/suggestions/")
        self.assertNotEqual(404, response.status_code)
