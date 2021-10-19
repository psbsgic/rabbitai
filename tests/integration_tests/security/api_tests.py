# isort:skip_file
# pylint: disable=too-many-public-methods, no-self-use, invalid-name, too-many-arguments
"""Unit tests for Superset"""
import json

from tests.integration_tests.base_tests import SupersetTestCase
from flask_wtf.csrf import generate_csrf


class TestSecurityApi(SupersetTestCase):
    resource_name = "security"

    def _assert_get_csrf_token(self):
        uri = f"api/v1/{self.resource_name}/csrf_token/"
        response = self.client.get(uri)
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert data["result"] == generate_csrf()

    def test_get_csrf_token(self):
        """
        Security API: Test get CSRF token
        """
        self.login(username="admin")
        self._assert_get_csrf_token()

    def test_get_csrf_token_gamma(self):
        """
        Security API: Test get CSRF token by gamma
        """
        self.login(username="gamma")
        self._assert_get_csrf_token()

    def test_get_csrf_unauthorized(self):
        """
        Security API: Test get CSRF no login
        """
        self.logout()
        uri = f"api/v1/{self.resource_name}/csrf_token/"
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 401)
