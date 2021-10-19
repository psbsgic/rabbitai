# -*- coding: utf-8 -*-

import importlib
import logging
from typing import Callable, Dict, TYPE_CHECKING

from flask import current_app, Flask, request, Response, session
from flask_login import login_user
from selenium.webdriver.remote.webdriver import WebDriver
from werkzeug.http import parse_cookie

from rabbitai.utils.urls import headless_url

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from flask_appbuilder.security.sqla.models import User


class MachineAuthProvider:
    """机器认证提供者。"""

    def __init__(
        self, auth_webdriver_func_override: Callable[[WebDriver, "User"], WebDriver]
    ):
        """
        使用指定Web驱动器认证函数，初始化新实例。

        :param auth_webdriver_func_override:
        """
        # This is here in order to allow for the authenticate_webdriver func to be
        # overridden via config, as opposed to the entire provider implementation
        self._auth_webdriver_func_override = auth_webdriver_func_override

    def authenticate_webdriver(self, driver: WebDriver, user: "User", ) -> WebDriver:
        """
        Default AuthDriverFuncType type that sets a session cookie flask-login style
        :return: The WebDriver passed in (fluent)
        """

        # Short-circuit this method if we have an override configured
        if self._auth_webdriver_func_override:
            return self._auth_webdriver_func_override(driver, user)

        # Setting cookies requires doing a request first
        driver.get(headless_url("/login/"))

        if user:
            cookies = self.get_auth_cookies(user)
        elif request.cookies:
            cookies = request.cookies
        else:
            cookies = {}

        for cookie_name, cookie_val in cookies.items():
            driver.add_cookie(dict(name=cookie_name, value=cookie_val))

        return driver

    @staticmethod
    def get_auth_cookies(user: "User") -> Dict[str, str]:
        # Login with the user specified to get the reports
        with current_app.test_request_context("/login"):
            login_user(user)
            # A mock response object to get the cookie information from
            response = Response()
            current_app.session_interface.save_session(current_app, session, response)

        cookies = {}

        # Grab any "set-cookie" headers from the login response
        for name, value in response.headers:
            if name.lower() == "set-cookie":
                # This yields a MultiDict, which is ordered -- something like
                # MultiDict([('session', 'value-we-want), ('HttpOnly', ''), etc...
                # Therefore, we just need to grab the first tuple and add it to our
                # final dict
                cookie = parse_cookie(value)
                cookie_tuple = list(cookie.items())[0]
                cookies[cookie_tuple[0]] = cookie_tuple[1]

        return cookies


class MachineAuthProviderFactory:
    """机器认证提供者工厂，提供访问 MachineAuthProvider 实例的功能。"""

    def __init__(self) -> None:
        self._auth_provider = None

    def init_app(self, app: Flask) -> None:
        """
        初始化，依据应用配置对象提供的 MACHINE_AUTH_PROVIDER_CLASS 选项值创建认证提供者实例。

        :param app:
        :return:
        """
        auth_provider_fqclass = app.config["MACHINE_AUTH_PROVIDER_CLASS"]
        auth_provider_classname = auth_provider_fqclass[
                                  auth_provider_fqclass.rfind(".") + 1:
                                  ]
        auth_provider_module_name = auth_provider_fqclass[
                                    0: auth_provider_fqclass.rfind(".")
                                    ]
        auth_provider_class = getattr(
            importlib.import_module(auth_provider_module_name), auth_provider_classname
        )

        self._auth_provider = auth_provider_class(app.config["WEBDRIVER_AUTH_FUNC"])

    @property
    def instance(self) -> MachineAuthProvider:
        return self._auth_provider  # type: ignore
