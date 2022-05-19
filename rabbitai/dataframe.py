# -*- coding: utf-8 -*-

""" pandas.DataFrame 实用工具函数。"""

import warnings
from typing import Any, Dict, List

import pandas as pd

from rabbitai.utils.core import JS_MAX_INTEGER


def _convert_big_integers(val: Any) -> Any:
    """
    转换大于 ``JS_MAX_INTEGER`` 的整数为字符串。

    :param val: 要处理的值。
    :returns: the same value but recast as a string if it was an integer over
        ``JS_MAX_INTEGER``
    """
    return str(val) if isinstance(val, int) and abs(val) > JS_MAX_INTEGER else val


def df_to_records(dframe: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    转换指定数据帧 DataFrame 为记录集合，即行数据字典的列表。

    :param dframe: 要转换的 DataFrame。
    :returns: 记录字典的列表。
    """

    if not dframe.columns.is_unique:
        warnings.warn(
            "DataFrame columns are not unique, some columns will be omitted.",
            UserWarning,
            stacklevel=2,
        )

    columns = dframe.columns

    return list(
        dict(zip(columns, map(_convert_big_integers, row)))
        for row in zip(*[dframe[col] for col in columns])
    )
