# -*- coding: utf-8 -*-

import re
import urllib.request
from typing import Any, Dict, Optional
from urllib.error import URLError

import pandas as pd

negative_number_re = re.compile(r"^-[0-9.]+$")

# This regex will match if the string starts with:
#
#     1. one of -, @, +, |, =, %
#     2. two double quotes immediately followed by one of -, @, +, |, =, %
#     3. one or more spaces immediately followed by one of -, @, +, |, =, %
#
problematic_chars_re = re.compile(r'^(?:"{2}|\s{1,})(?=[\-@+|=%])|^[\-@+|=%]')


def escape_value(value: str) -> str:
    """
    Escapes a set of special characters.

    http://georgemauer.net/2017/10/07/csv-injection.html
    """
    needs_escaping = problematic_chars_re.match(value) is not None
    is_negative_number = negative_number_re.match(value) is not None

    if needs_escaping and not is_negative_number:
        # Escape pipe to be extra safe as this
        # can lead to remote code execution
        value = value.replace("|", "\\|")

        # Precede the line with a single quote. This prevents
        # evaluation of commands and some spreadsheet software
        # will hide this visually from the user. Many articles
        # claim a preceding space will work here too, however,
        # when uploading a csv file in Google sheets, a leading
        # space was ignored and code was still evaluated.
        value = "'" + value

    return value


def df_to_escaped_csv(df: pd.DataFrame, **kwargs: Any) -> Any:
    escape_values = lambda v: escape_value(v) if isinstance(v, str) else v

    # Escape csv headers
    df = df.rename(columns=escape_values)

    # Escape csv rows
    df = df.applymap(escape_values)

    return df.to_csv(**kwargs)


def get_chart_csv_data(
    chart_url: str, auth_cookies: Optional[Dict[str, str]] = None
) -> Optional[bytes]:
    content = None
    if auth_cookies:
        opener = urllib.request.build_opener()
        cookie_str = ";".join([f"{key}={val}" for key, val in auth_cookies.items()])
        opener.addheaders.append(("Cookie", cookie_str))
        response = opener.open(chart_url)
        content = response.read()
    if response.getcode() != 200:
        raise URLError(response.getcode())
    if content:
        return content
    return None
