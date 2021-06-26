# -*- coding: utf-8 -*-

from flask import Flask
from flask_caching import Cache


class CacheManager:
    """缓存管理器，依据Flask应用配置信息，创建缓存、数据缓存、THUMBNAIL缓存。"""

    def __init__(self) -> None:
        super().__init__()

        self._cache = Cache()
        self._data_cache = Cache()
        self._thumbnail_cache = Cache()

    def init_app(self, app: Flask) -> None:
        """
        依据Flask应用配置信息，创建缓存、数据缓存、THUMBNAIL缓存。

        :param app: Flask应用.
        :return:
        """

        self._cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["CACHE_CONFIG"],
            },
        )
        self._data_cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["DATA_CACHE_CONFIG"],
            },
        )
        self._thumbnail_cache.init_app(
            app,
            {
                "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
                **app.config["THUMBNAIL_CACHE_CONFIG"],
            },
        )

    @property
    def data_cache(self) -> Cache:
        return self._data_cache

    @property
    def cache(self) -> Cache:
        return self._cache

    @property
    def thumbnail_cache(self) -> Cache:
        return self._thumbnail_cache
