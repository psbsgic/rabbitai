# -*- coding: utf-8 -*-

import json
import os
from typing import Any, Callable, Dict, List, Optional

import celery
from cachelib.base import BaseCache
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from werkzeug.local import LocalProxy

from rabbitai.utils.async_query_manager import AsyncQueryManager
from rabbitai.utils.cache_manager import CacheManager
from rabbitai.utils.encrypt import EncryptedFieldFactory
from rabbitai.utils.feature_flag_manager import FeatureFlagManager
from rabbitai.utils.machine_auth import MachineAuthProviderFactory


class ResultsBackendManager:
    """结果后端管理器，从应用配置 RESULTS_BACKEND、RESULTS_BACKEND_USE_MSGPACK分别获取后端和消息打包方式。"""

    def __init__(self) -> None:
        self._results_backend = None
        self._use_msgpack = False

    def init_app(self, app: Flask) -> None:
        """
        从应用配置 RESULTS_BACKEND、RESULTS_BACKEND_USE_MSGPACK分别获取后端和消息打包方式。

        :param app: Flask 及其派生类型实例。

        :return:
        """
        self._results_backend = app.config["RESULTS_BACKEND"]
        self._use_msgpack = app.config["RESULTS_BACKEND_USE_MSGPACK"]

    @property
    def results_backend(self) -> Optional[BaseCache]:
        """获取存储结果的后端，BaseCache派生类型。"""
        return self._results_backend

    @property
    def should_use_msgpack(self) -> bool:
        """是否使用 msgpack 序列化。"""
        return self._use_msgpack


class UIManifestProcessor:
    """应用UI资源清单处理器，主要管理 /static/assets/manifest.json中定义的资源。

    打包：

    preamble，theme，menu，spa，addSlice，explore，sqllab，profile，showSavedQuery。
    """

    def __init__(self, app_dir: str) -> None:
        self.app: Optional[Flask] = None
        self.manifest: Dict[str, Dict[str, List[str]]] = {}
        self.manifest_file = f"{app_dir}/static/assets/manifest.json"

    def init_app(self, app: Flask) -> None:
        """
        依据指定应用对象初始化该对象实例，解析相关资源。

        :param app: Flask 及其派生类型实例。
        :return:
        """

        self.app = app
        # 预加载缓存
        self.parse_manifest_json()

        @app.context_processor
        def get_manifest() -> Dict[str, Callable[[str], List[str]]]:
            """
            获取资源清单，即js_manifest、css_manifest资源加载的字典。
            可以让所有自定义变量 js_manifest、css_manifest 在所有模板中全局可访问

            :return:
            """

            loaded_chunks = set()

            def get_files(bundle: str, asset_type: str = "js") -> List[str]:
                files = self.get_manifest_files(bundle, asset_type)
                filtered_files = [f for f in files if f not in loaded_chunks]
                for f in filtered_files:
                    loaded_chunks.add(f)
                return filtered_files

            return dict(
                js_manifest=lambda bundle: get_files(bundle, "js"),
                css_manifest=lambda bundle: get_files(bundle, "css"),
            )

    def parse_manifest_json(self) -> None:
        """解析资源清单文件，即 entrypoints 的值。"""

        try:
            with open(self.manifest_file, "r") as f:
                # 清单包括非条目文件，我们只需要模板中的条目
                full_manifest = json.load(f)
                self.manifest = full_manifest.get("entrypoints", {})
        except Exception:
            pass

    def get_manifest_files(self, bundle: str, asset_type: str) -> List[str]:
        """
        获取指定打包名称和资源类型的所有清单文件。

        :param bundle: 打包名称。
        :param asset_type: 资源类型。
        :return:
        """

        if self.app and self.app.debug:
            self.parse_manifest_json()
        return self.manifest.get(bundle, {}).get(asset_type, [])


APP_DIR = os.path.dirname(__file__)
"""应用根目录，即该文件所在目录"""
appbuilder = AppBuilder(update_perms=False)
"""应用程序构建者"""
async_query_manager = AsyncQueryManager()
"""异步查询管理器"""
cache_manager = CacheManager()
"""缓存管理器"""
celery_app = celery.Celery()
"""并发分布式应用"""
csrf = CSRFProtect()
"""跨站保护"""
db = SQLA()
"""数据库"""
_event_logger: Dict[str, Any] = {}
"""事件日志字典"""
encrypted_field_factory = EncryptedFieldFactory()
"""加密字段工厂"""
event_logger = LocalProxy(lambda: _event_logger.get("event_logger"))
"""事件日志记录器"""
feature_flag_manager = FeatureFlagManager()
"""特性（功能）标志管理器"""
machine_auth_provider_factory = MachineAuthProviderFactory()
"""机器认证提供者工厂"""
manifest_processor = UIManifestProcessor(APP_DIR)
"""资源清单处理器，管理应用程序中的资源"""
migrate = Migrate()
"""数据库迁移对象"""
results_backend_manager = ResultsBackendManager()
"""结果后端管理器"""
security_manager = LocalProxy(lambda: appbuilder.sm)
"""安全管理器"""
talisman = Talisman()
"""Http安全标头管理"""
