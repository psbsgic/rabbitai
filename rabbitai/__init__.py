# -*- coding: utf-8 -*-

"""软件包的主模块!"""

from flask import current_app, Flask
from werkzeug.local import LocalProxy

from rabbitai.app import create_app
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.extensions import (
    appbuilder,
    cache_manager,
    db,
    event_logger,
    feature_flag_manager,
    manifest_processor,
    results_backend_manager,
    security_manager,
    talisman,
)
from rabbitai.security import RabbitaiSecurityManager

# 此处的所有字段都应视为遗留字段。声明“全局（global）”依赖关系的正确方法是在extensions.py中声明,
# 然后在app.create_app()中初始化它。这些字段将移除。
app: Flask = current_app
cache = cache_manager.cache
conf = LocalProxy(lambda: current_app.config)
get_feature_flags = feature_flag_manager.get_feature_flags
get_manifest_files = manifest_processor.get_manifest_files
is_feature_enabled = feature_flag_manager.is_feature_enabled
results_backend = LocalProxy(lambda: results_backend_manager.results_backend)
results_backend_use_msgpack = LocalProxy(
    lambda: results_backend_manager.should_use_msgpack
)
data_cache = LocalProxy(lambda: cache_manager.data_cache)
thumbnail_cache = LocalProxy(lambda: cache_manager.thumbnail_cache)
