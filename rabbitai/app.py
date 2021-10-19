# -*- coding: utf-8 -*-

import logging
import os

from flask import Flask

from rabbitai.initialization import RabbitaiAppInitializer

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """创建并返回Rabbitai应用服务器，即 Flask 派生类型实例。"""

    app = RabbitaiApp(__name__)

    try:
        # 运行用户通过环境变量指定配置模块对应用进行配置
        config_module = os.environ.get("RABBITAI_CONFIG", "rabbitai.config")
        app.config.from_object(config_module)

        # 初始化应用，加载相关视图等
        app_initializer = app.config.get("APP_INITIALIZER", RabbitaiAppInitializer)(app)
        app_initializer.init_app()

        return app

    except Exception as ex:
        logger.exception("创建应用服务器失败！")
        raise ex


class RabbitaiApp(Flask):
    """Rabbitai应用服务器，扩展 Flask。"""
    pass
