""" Rabbitai utilities for pandas.DataFrame.
"""
import warnings
from typing import Any, Dict, List

import pandas as pd

from rabbitai.utils.core import JS_MAX_INTEGER


def _convert_big_integers(val: Any) -> Any:
    """
    Cast integers larger than ``JS_MAX_INTEGER`` to strings.

    :param val: the value to process
    :returns: the same value but recast as a string if it was an integer over
        ``JS_MAX_INTEGER``
    """
    return str(val) if isinstance(val, int) and abs(val) > JS_MAX_INTEGER else val


def df_to_records(dframe: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a DataFrame to a set of records.

    :param dframe: the DataFrame to convert
    :returns: a list of dictionaries reflecting each single row of the DataFrame
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
