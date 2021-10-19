from .base_tests import SupersetTestCase
from .conftest import with_feature_flags


class TestDynamicPlugins(SupersetTestCase):
    @with_feature_flags(DYNAMIC_PLUGINS=False)
    def test_dynamic_plugins_disabled(self):
        """
        Dynamic Plugins: Responds not found when disabled
        """
        self.login(username="admin")
        uri = "/dynamic-plugins/api"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(DYNAMIC_PLUGINS=True)
    def test_dynamic_plugins_enabled(self):
        """
        Dynamic Plugins: Responds successfully when enabled
        """
        self.login(username="admin")
        uri = "/dynamic-plugins/api"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 200)
