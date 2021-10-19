# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Any, Dict

from flask import Flask


class FeatureFlagManager:
    """特性（功能）标志管理器，提供从应用配置价值功能标志并进行管理的功能。"""

    def __init__(self) -> None:
        super().__init__()
        self._get_feature_flags_func = None
        self._feature_flags: Dict[str, Any] = {}

    def init_app(self, app: Flask) -> None:
        """
        初始化，从应用配置中加载GET_FEATURE_FLAGS_FUNC、DEFAULT_FEATURE_FLAGS、FEATURE_FLAGS
        :param app:
        :return:
        """
        self._get_feature_flags_func = app.config["GET_FEATURE_FLAGS_FUNC"]
        self._feature_flags = app.config["DEFAULT_FEATURE_FLAGS"]
        self._feature_flags.update(app.config["FEATURE_FLAGS"])

    def get_feature_flags(self) -> Dict[str, Any]:
        """获取应用定义的功能标志字典。"""
        if self._get_feature_flags_func:
            return self._get_feature_flags_func(deepcopy(self._feature_flags))

        return self._feature_flags

    def is_feature_enabled(self, feature: str) -> bool:
        """Utility function for checking whether a feature is turned on"""

        feature_flags = self.get_feature_flags()

        if feature_flags and feature in feature_flags:
            return feature_flags[feature]

        return False
