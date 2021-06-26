from unittest.mock import patch

from rabbitai.views.log.views import LogModelView

from .base_tests import RabbitaiTestCase


class TestLogModelView(RabbitaiTestCase):
    def test_disabled(self):
        with patch.object(LogModelView, "is_enabled", return_value=False):
            self.login("admin")
            uri = "/logmodelview/list/"
            rv = self.client.get(uri)
            self.assert404(rv)

    def test_enabled(self):
        with patch.object(LogModelView, "is_enabled", return_value=True):
            self.login("admin")
            uri = "/logmodelview/list/"
            rv = self.client.get(uri)
            self.assert200(rv)
