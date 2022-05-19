# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Generator, List, Optional, Type

import backoff


def retry_call(
    func: Callable[..., Any],
    *args: Any,
    strategy: Callable[..., Generator[int, None, None]] = backoff.constant,
    exception: Type[Exception] = Exception,
    fargs: Optional[List[Any]] = None,
    fkwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> Any:
    """
    尝试调用被装饰函数。

    :param func:
    :param args:
    :param strategy:
    :param exception:
    :param fargs:
    :param fkwargs:
    :param kwargs:
    :return:
    """

    decorated = backoff.on_exception(strategy, exception, *args, **kwargs)(func)
    fargs = fargs or []
    fkwargs = fkwargs or {}

    return decorated(*fargs, **fkwargs)
