from tests.base_tests import RabbitaiTestCase
from tests.conftest import with_feature_flags


class TestRowLevelSecurityFiltersModelView(RabbitaiTestCase):
    @with_feature_flags(ROW_LEVEL_SECURITY=False)
    def test_rls_disabled(self):
        """
        RLS Filters Model View: Responds not found when disabled
        """
        self.login(username="admin")
        uri = "/rowlevelsecurityfiltersmodelview/api"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(ROW_LEVEL_SECURITY=True)
    def test_rls_enabled(self):
        """
        RLS Filters Model View: Responds successfully when enabled
        """
        self.login(username="admin")
        uri = "/rowlevelsecurityfiltersmodelview/api"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 200)
