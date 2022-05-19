# -*- coding: utf-8 -*-

import hashlib
from typing import Any, Callable, Dict, Optional

import simplejson as json


def md5_sha_from_str(val: str) -> str:
    """
    返回使用 md5 算法的哈希码字符串。

    :param val: 字符串值。
    :type val: str
    :return:
    :rtype: str
    """
    return hashlib.md5(val.encode("utf-8")).hexdigest()


def md5_sha_from_dict(
    obj: Dict[Any, Any],
    ignore_nan: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
) -> str:
    """
    使用 MD5 算法返回指定字典的哈希码字符串。

    :param obj: 字典对象。
    :type obj:
    :param ignore_nan:
    :type ignore_nan:
    :param default:
    :type default:
    :return:
    :rtype:
    """

    json_data = json.dumps(obj, sort_keys=True, ignore_nan=ignore_nan, default=default)

    return md5_sha_from_str(json_data)
