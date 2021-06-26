# pylint: disable=no-self-use
import pytest

from rabbitai.utils.core import to_adhoc


def test_to_adhoc_generates_deterministic_values():
    input_1 = {
        "op": "IS NOT NULL",
        "col": "LATITUDE",
        "val": "",
    }

    input_2 = {**input_1, "col": "LONGITUDE"}

    # The result is the same when given the same input
    assert to_adhoc(input_1) == to_adhoc(input_1)
    assert to_adhoc(input_1) == {
        "clause": "WHERE",
        "expressionType": "SIMPLE",
        "isExtra": False,
        "comparator": "",
        "operator": "IS NOT NULL",
        "subject": "LATITUDE",
        "filterOptionName": "d0908f77d950131db7a69fdc820cb739",
    }

    # The result is different when given different input
    assert to_adhoc(input_1) != to_adhoc(input_2)
    assert to_adhoc(input_2) == {
        "clause": "WHERE",
        "expressionType": "SIMPLE",
        "isExtra": False,
        "comparator": "",
        "operator": "IS NOT NULL",
        "subject": "LONGITUDE",
        "filterOptionName": "c5f283f727d4dfc6258b351d4a8663bc",
    }
