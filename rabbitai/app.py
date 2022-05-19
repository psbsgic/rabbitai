# -*- coding: utf-8 -*-

import logging
import os

from flask import Flask

from rabbitai.initialization import RabbitaiAppInitializer

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    创建并返回 RabbitAI 应用服务器，即 Flask 派生类型实例。

    - 依据环境变量 RABBITAI_CONFIG 的值获取配置模块名称，默认：rabbitai.config，将配置模块导入到应用的 config 属性。
    - 依据应用配置对象 APP_INITIALIZER 的值获取初始化器模块名称，默认：RabbitaiAppInitializer实例。
    - 调用初始化器模块的 init_app() 方法，初始化应用，加载相关视图等。
    """

    app = RabbitaiApp(__name__)

    try:
        # 通过环境变量指定配置模块对应用进行配置
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
    """RabbitAI 应用服务器，扩展 Flask。"""
    pass
