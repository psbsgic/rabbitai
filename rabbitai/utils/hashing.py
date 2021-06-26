# -*- coding: utf-8 -*-

import hashlib
from typing import Any, Callable, Dict, Optional

import simplejson as json


def md5_sha_from_str(val: str) -> str:
    return hashlib.md5(val.encode("utf-8")).hexdigest()


def md5_sha_from_dict(
    obj: Dict[Any, Any],
    ignore_nan: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
) -> str:
    json_data = json.dumps(obj, sort_keys=True, ignore_nan=ignore_nan, default=default)

    return md5_sha_from_str(json_data)
