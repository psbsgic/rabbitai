# from rabbitai import db
# from rabbitai.models.dashboard import Dashboard
import urllib.request
from io import BytesIO
from unittest import skipUnless
from unittest.mock import ANY, call, patch

from flask_testing import LiveServerTestCase
from sqlalchemy.sql import func

from rabbitai import db, is_feature_enabled, security_manager
from rabbitai.extensions import machine_auth_provider_factory
from rabbitai.models.dashboard import Dashboard
from rabbitai.models.slice import Slice
from rabbitai.utils.screenshots import ChartScreenshot, DashboardScreenshot
from rabbitai.utils.urls import get_url_host, get_url_path
from rabbitai.utils.webdriver import WebDriverProxy
from tests.integration_tests.conftest import with_feature_flags
from tests.integration_tests.test_app import app

from .base_tests import SupersetTestCase


class TestThumbnailsSeleniumLive(LiveServerTestCase):
    def create_app(self):
        return app

    def url_open_auth(self, username: str, url: str):
        admin_user = security_manager.find_user(username=username)
        cookies = machine_auth_provider_factory.instance.get_auth_cookies(admin_user)
        opener = urllib.request.build_opener()
        opener.addheaders.append(("Cookie", f"session={cookies['session']}"))
        return opener.open(f"{self.get_server_url()}/{url}")

    @skipUnless((is_feature_enabled("THUMBNAILS")), "Thumbnails feature")
    def test_get_async_dashboard_screenshot(self):
        """
        Thumbnails: Simple get async dashboard screenshot
        """
        dashboard = db.session.query(Dashboard).all()[0]
        with patch("rabbitai.dashboards.api.DashboardRestApi.get") as mock_get:
            response = self.url_open_auth(
                "admin",
                f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/",
            )
            self.assertEqual(response.getcode(), 202)


class TestWebDriverProxy(SupersetTestCase):
    @patch("rabbitai.utils.webdriver.WebDriverWait")
    @patch("rabbitai.utils.webdriver.firefox")
    @patch("rabbitai.utils.webdriver.sleep")
    def test_screenshot_selenium_headstart(
        self, mock_sleep, mock_webdriver, mock_webdriver_wait
    ):
        webdriver = WebDriverProxy("firefox")
        user = security_manager.get_user_by_username(
            app.config["THUMBNAIL_SELENIUM_USER"]
        )
        url = get_url_path("Superset.slice", slice_id=1, standalone="true")
        app.config["SCREENSHOT_SELENIUM_HEADSTART"] = 5
        webdriver.get_screenshot(url, "chart-container", user=user)
        assert mock_sleep.call_args_list[0] == call(5)

    @patch("rabbitai.utils.webdriver.WebDriverWait")
    @patch("rabbitai.utils.webdriver.firefox")
    def test_screenshot_selenium_locate_wait(self, mock_webdriver, mock_webdriver_wait):
        app.config["SCREENSHOT_LOCATE_WAIT"] = 15
        webdriver = WebDriverProxy("firefox")
        user = security_manager.get_user_by_username(
            app.config["THUMBNAIL_SELENIUM_USER"]
        )
        url = get_url_path("Superset.slice", slice_id=1, standalone="true")
        webdriver.get_screenshot(url, "chart-container", user=user)
        assert mock_webdriver_wait.call_args_list[0] == call(ANY, 15)

    @patch("rabbitai.utils.webdriver.WebDriverWait")
    @patch("rabbitai.utils.webdriver.firefox")
    def test_screenshot_selenium_load_wait(self, mock_webdriver, mock_webdriver_wait):
        app.config["SCREENSHOT_LOAD_WAIT"] = 15
        webdriver = WebDriverProxy("firefox")
        user = security_manager.get_user_by_username(
            app.config["THUMBNAIL_SELENIUM_USER"]
        )
        url = get_url_path("Superset.slice", slice_id=1, standalone="true")
        webdriver.get_screenshot(url, "chart-container", user=user)
        assert mock_webdriver_wait.call_args_list[1] == call(ANY, 15)

    @patch("rabbitai.utils.webdriver.WebDriverWait")
    @patch("rabbitai.utils.webdriver.firefox")
    @patch("rabbitai.utils.webdriver.sleep")
    def test_screenshot_selenium_animation_wait(
        self, mock_sleep, mock_webdriver, mock_webdriver_wait
    ):
        webdriver = WebDriverProxy("firefox")
        user = security_manager.get_user_by_username(
            app.config["THUMBNAIL_SELENIUM_USER"]
        )
        url = get_url_path("Superset.slice", slice_id=1, standalone="true")
        app.config["SCREENSHOT_SELENIUM_ANIMATION_WAIT"] = 4
        webdriver.get_screenshot(url, "chart-container", user=user)
        assert mock_sleep.call_args_list[1] == call(4)


class TestThumbnails(SupersetTestCase):

    mock_image = b"bytes mock image"

    @with_feature_flags(THUMBNAILS=False)
    def test_dashboard_thumbnail_disabled(self):
        """
        Thumbnails: Dashboard thumbnail disabled
        """
        dashboard = db.session.query(Dashboard).all()[0]
        self.login(username="admin")
        uri = f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(THUMBNAILS=False)
    def test_chart_thumbnail_disabled(self):
        """
        Thumbnails: Chart thumbnail disabled
        """
        chart = db.session.query(Slice).all()[0]
        self.login(username="admin")
        uri = f"api/v1/chart/{chart}/thumbnail/{chart.digest}/"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(THUMBNAILS=True)
    def test_get_async_dashboard_screenshot(self):
        """
        Thumbnails: Simple get async dashboard screenshot
        """
        dashboard = db.session.query(Dashboard).all()[0]
        self.login(username="admin")
        uri = f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/"
        with patch(
            "rabbitai.tasks.thumbnails.cache_dashboard_thumbnail.delay"
        ) as mock_task:
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 202)

            expected_uri = f"{get_url_host()}rabbitai/dashboard/{dashboard.id}/"
            expected_digest = dashboard.digest
            expected_kwargs = {"force": True}
            mock_task.assert_called_with(
                expected_uri, expected_digest, **expected_kwargs
            )

    @with_feature_flags(THUMBNAILS=True)
    def test_get_async_dashboard_notfound(self):
        """
        Thumbnails: Simple get async dashboard not found
        """
        max_id = db.session.query(func.max(Dashboard.id)).scalar()
        self.login(username="admin")
        uri = f"api/v1/dashboard/{max_id + 1}/thumbnail/1234/"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @skipUnless((is_feature_enabled("THUMBNAILS")), "Thumbnails feature")
    def test_get_async_dashboard_not_allowed(self):
        """
        Thumbnails: Simple get async dashboard not allowed
        """
        dashboard = db.session.query(Dashboard).all()[0]
        self.login(username="gamma")
        uri = f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(THUMBNAILS=True)
    def test_get_async_chart_screenshot(self):
        """
        Thumbnails: Simple get async chart screenshot
        """
        chart = db.session.query(Slice).all()[0]
        self.login(username="admin")
        uri = f"api/v1/chart/{chart.id}/thumbnail/{chart.digest}/"
        with patch(
            "rabbitai.tasks.thumbnails.cache_chart_thumbnail.delay"
        ) as mock_task:
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 202)
            expected_uri = f"{get_url_host()}rabbitai/slice/{chart.id}/?standalone=true"
            expected_digest = chart.digest
            expected_kwargs = {"force": True}
            mock_task.assert_called_with(
                expected_uri, expected_digest, **expected_kwargs
            )

    @with_feature_flags(THUMBNAILS=True)
    def test_get_async_chart_notfound(self):
        """
        Thumbnails: Simple get async chart not found
        """
        max_id = db.session.query(func.max(Slice.id)).scalar()
        self.login(username="admin")
        uri = f"api/v1/chart/{max_id + 1}/thumbnail/1234/"
        rv = self.client.get(uri)
        self.assertEqual(rv.status_code, 404)

    @with_feature_flags(THUMBNAILS=True)
    def test_get_cached_chart_wrong_digest(self):
        """
        Thumbnails: Simple get chart with wrong digest
        """
        chart = db.session.query(Slice).all()[0]
        with patch.object(
            ChartScreenshot, "get_from_cache", return_value=BytesIO(self.mock_image)
        ):
            self.login(username="admin")
            uri = f"api/v1/chart/{chart.id}/thumbnail/1234/"
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 302)
            self.assertRedirects(
                rv, f"api/v1/chart/{chart.id}/thumbnail/{chart.digest}/"
            )

    @with_feature_flags(THUMBNAILS=True)
    def test_get_cached_dashboard_screenshot(self):
        """
        Thumbnails: Simple get cached dashboard screenshot
        """
        dashboard = db.session.query(Dashboard).all()[0]
        with patch.object(
            DashboardScreenshot, "get_from_cache", return_value=BytesIO(self.mock_image)
        ):
            self.login(username="admin")
            uri = f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/"
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, self.mock_image)

    @with_feature_flags(THUMBNAILS=True)
    def test_get_cached_chart_screenshot(self):
        """
        Thumbnails: Simple get cached chart screenshot
        """
        chart = db.session.query(Slice).all()[0]
        with patch.object(
            ChartScreenshot, "get_from_cache", return_value=BytesIO(self.mock_image)
        ):
            self.login(username="admin")
            uri = f"api/v1/chart/{chart.id}/thumbnail/{chart.digest}/"
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, self.mock_image)

    @with_feature_flags(THUMBNAILS=True)
    def test_get_cached_dashboard_wrong_digest(self):
        """
        Thumbnails: Simple get dashboard with wrong digest
        """
        dashboard = db.session.query(Dashboard).all()[0]
        with patch.object(
            DashboardScreenshot, "get_from_cache", return_value=BytesIO(self.mock_image)
        ):
            self.login(username="admin")
            uri = f"api/v1/dashboard/{dashboard.id}/thumbnail/1234/"
            rv = self.client.get(uri)
            self.assertEqual(rv.status_code, 302)
            self.assertRedirects(
                rv, f"api/v1/dashboard/{dashboard.id}/thumbnail/{dashboard.digest}/"
            )
