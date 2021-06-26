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
    """结果后端管理器，提供后端缓存和是否使用 msgpack。"""

    def __init__(self) -> None:
        self._results_backend = None
        self._use_msgpack = False

    def init_app(self, app: Flask) -> None:
        self._results_backend = app.config["RESULTS_BACKEND"]
        self._use_msgpack = app.config["RESULTS_BACKEND_USE_MSGPACK"]

    @property
    def results_backend(self) -> Optional[BaseCache]:
        return self._results_backend

    @property
    def should_use_msgpack(self) -> bool:
        return self._use_msgpack


class UIManifestProcessor:
    """UI资源文件处理器，提供从给定资源目录文件{{app_dir}/static/assets/manifest.json}中加载JS、CSS等资源的功能。"""

    def __init__(self, app_dir: str) -> None:
        self.app: Optional[Flask] = None
        self.manifest: Dict[str, Dict[str, List[str]]] = {}
        self.manifest_file = f"{app_dir}/static/assets/manifest.json"

    def init_app(self, app: Flask) -> None:
        self.app = app
        # Preload the cache
        self.parse_manifest_json()

        @app.context_processor
        def get_manifest() -> Dict[str, Callable[[str], List[str]]]:
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
        try:
            with open(self.manifest_file, "r") as f:
                # the manifest includes non-entry files we only need entries in templates
                full_manifest = json.load(f)
                self.manifest = full_manifest.get("entrypoints", {})
        except Exception:
            pass

    def get_manifest_files(self, bundle: str, asset_type: str) -> List[str]:
        if self.app and self.app.debug:
            self.parse_manifest_json()
        return self.manifest.get(bundle, {}).get(asset_type, [])


APP_DIR = os.path.dirname(__file__)
appbuilder = AppBuilder(update_perms=False)
async_query_manager = AsyncQueryManager()
cache_manager = CacheManager()
celery_app = celery.Celery()
csrf = CSRFProtect()
db = SQLA()
_event_logger: Dict[str, Any] = {}
encrypted_field_factory = EncryptedFieldFactory()
event_logger = LocalProxy(lambda: _event_logger.get("event_logger"))
feature_flag_manager = FeatureFlagManager()
machine_auth_provider_factory = MachineAuthProviderFactory()
manifest_processor = UIManifestProcessor(APP_DIR)
migrate = Migrate()
results_backend_manager = ResultsBackendManager()
security_manager = LocalProxy(lambda: appbuilder.sm)
talisman = Talisman()
