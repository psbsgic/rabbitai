# -*- coding: utf-8 -*-

import urllib
from typing import Any

from flask import current_app, url_for


def get_url_host(user_friendly: bool = False) -> str:
    """
    从当前Web应用的配置对象中获取主机地址 WEBDRIVER_BASEURL_USER_FRIENDLY 或 WEBDRIVER_BASEURL配置选项的值。

    :param user_friendly: 是否用户友好的，默认False。
    :return:
    """

    if user_friendly:
        return current_app.config["WEBDRIVER_BASEURL_USER_FRIENDLY"]
    return current_app.config["WEBDRIVER_BASEURL"]


def headless_url(path: str, user_friendly: bool = False) -> str:
    """
    获取无标头的地址，基地址 + 路径。

    :param path: 路径字符串。
    :param user_friendly:
    :return:
    """

    return urllib.parse.urljoin(get_url_host(user_friendly=user_friendly), path)


def get_url_path(view: str, user_friendly: bool = False, **kwargs: Any) -> str:
    """
    获取完整地址路径。

    :param view: 视图名称。
    :param user_friendly: 是否友好的，默认False
    :param kwargs: 其它参数。
    :return:
    """

    with current_app.test_request_context():
        return headless_url(url_for(view, **kwargs), user_friendly=user_friendly)
