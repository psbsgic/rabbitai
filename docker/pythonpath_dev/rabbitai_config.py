# -*- coding: utf-8 -*-

"""
该文件要包括在最终的 Docker 镜像中，部署镜像到生产环境时应该重写。
这里设置的配置值打算用于本地开发环境。
也应该注意到最后导入 rabbitai_config_docker.py 重写这里的默认值。
"""

import logging
import os
from datetime import timedelta
from typing import Optional

from cachelib.file import FileSystemCache
from celery.schedules import crontab

logger = logging.getLogger()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    获取环境变量或引发异常。

    :param var_name: 环境变量。
    :param default: 默认值。
    :return: 环境变量的值。
    """

    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "环境变量 {} 不存在，终止...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


# region SQLAlchemy 连接字符串

DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

"""
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)
"""
SQLALCHEMY_DATABASE_URI = f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}" \
                          f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

# endregion

# region CeleryConfig

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/rabbitai_home/sqllab")


class CeleryConfig(object):
    """Celery 配置对象，基于环境变量：REDIS_HOST、REDIS_PORT、REDIS_CELERY_DB、REDIS_RESULTS_DB构建"""
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("rabbitai.sql_lab", "rabbitai.tasks")
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# endregion

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://rabbitai:8088/"
# Email报告超链接地址
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True

#
# 可选导入 rabbitai_config_docker.py (它位于 PYTHONPATH) 以允许覆盖本地设置
#
try:
    import rabbitai_config_docker
    from rabbitai_config_docker import *  # noqa

    logger.info(
        f"已加载 Docker 配置[{rabbitai_config_docker.__file__}]"
    )
except ImportError:
    logger.info("使用默认 Docker 配置...")
