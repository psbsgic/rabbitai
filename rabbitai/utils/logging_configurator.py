# -*- coding: utf-8 -*-

import abc
import logging
from logging.handlers import TimedRotatingFileHandler

import flask.app
import flask.config

logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class LoggingConfigurator(abc.ABC):
    @abc.abstractmethod
    def configure_logging(
        self, app_config: flask.config.Config, debug_mode: bool
    ) -> None:
        pass


class DefaultLoggingConfigurator(LoggingConfigurator):
    def configure_logging(
        self, app_config: flask.config.Config, debug_mode: bool
    ) -> None:
        if app_config["SILENCE_FAB"]:
            logging.getLogger("flask_appbuilder").setLevel(logging.ERROR)

        # configure rabbitai app logger
        rabbitai_logger = logging.getLogger("rabbitai")
        if debug_mode:
            rabbitai_logger.setLevel(logging.DEBUG)
        else:
            # In production mode, add log handler to sys.stderr.
            rabbitai_logger.addHandler(logging.StreamHandler())
            rabbitai_logger.setLevel(logging.INFO)

        logging.getLogger("pyhive.presto").setLevel(logging.INFO)

        logging.basicConfig(format=app_config["LOG_FORMAT"])
        logging.getLogger().setLevel(app_config["LOG_LEVEL"])

        if app_config["ENABLE_TIME_ROTATE"]:
            logging.getLogger().setLevel(app_config["TIME_ROTATE_LOG_LEVEL"])
            handler = TimedRotatingFileHandler(
                app_config["FILENAME"],
                when=app_config["ROLLOVER"],
                interval=app_config["INTERVAL"],
                backupCount=app_config["BACKUP_COUNT"],
            )
            logging.getLogger().addHandler(handler)

        logger.info("logging was configured successfully")
