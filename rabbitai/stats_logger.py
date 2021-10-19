# -*- coding: utf-8 -*-

import logging
from typing import Optional

from colorama import Fore, Style

logger = logging.getLogger(__name__)


class BaseStatsLogger:
    """Base class for logging realtime events"""

    def __init__(self, prefix: str = "rabbitai") -> None:
        self.prefix = prefix

    def key(self, key: str) -> str:
        if self.prefix:
            return self.prefix + key
        return key

    def incr(self, key: str) -> None:
        """Increment a counter"""
        raise NotImplementedError()

    def decr(self, key: str) -> None:
        """Decrement a counter"""
        raise NotImplementedError()

    def timing(self, key: str, value: float) -> None:
        raise NotImplementedError()

    def gauge(self, key: str, value: float) -> None:
        """Setup a gauge"""
        raise NotImplementedError()


class DummyStatsLogger(BaseStatsLogger):
    def incr(self, key: str) -> None:
        logger.debug(Fore.CYAN + "[stats_logger] (incr) " + key + Style.RESET_ALL)

    def decr(self, key: str) -> None:
        logger.debug((Fore.CYAN + "[stats_logger] (decr) " + key + Style.RESET_ALL))

    def timing(self, key: str, value: float) -> None:
        logger.debug(
            (Fore.CYAN + f"[stats_logger] (timing) {key} | {value} " + Style.RESET_ALL)
        )

    def gauge(self, key: str, value: float) -> None:
        logger.debug(
            (
                Fore.CYAN
                + "[stats_logger] (gauge) "
                + f"{key}"
                + f"{value}"
                + Style.RESET_ALL
            )
        )


try:
    from statsd import StatsClient

    class StatsdStatsLogger(BaseStatsLogger):
        def __init__(  # pylint: disable=super-init-not-called
            self,
            host: str = "localhost",
            port: int = 8125,
            prefix: str = "rabbitai",
            statsd_client: Optional[StatsClient] = None,
        ) -> None:
            """
            Initializes from either params or a supplied, pre-constructed statsd client.

            If statsd_client argument is given, all other arguments are ignored and the
            supplied client will be used to emit metrics.
            """
            if statsd_client:
                self.client = statsd_client
            else:
                self.client = StatsClient(host=host, port=port, prefix=prefix)

        def incr(self, key: str) -> None:
            self.client.incr(key)

        def decr(self, key: str) -> None:
            self.client.decr(key)

        def timing(self, key: str, value: float) -> None:
            self.client.timing(key, value)

        def gauge(self, key: str, value: float) -> None:
            self.client.gauge(key, value)


except Exception:  # pylint: disable=broad-except
    pass
