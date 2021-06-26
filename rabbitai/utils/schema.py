# -*- coding: utf-8 -*-

from typing import Any, Union

from marshmallow import validate, ValidationError

from rabbitai.exceptions import RabbitaiException
from rabbitai.utils import core as utils


class OneOfCaseInsensitive(validate.OneOf):
    """
    Marshmallow validator that's based on the built-in `OneOf`, but performs
    validation case insensitively.
    """

    def __call__(self, value: Any) -> str:
        try:
            if (value.lower() if isinstance(value, str) else value) not in [
                choice.lower() if isinstance(choice, str) else choice
                for choice in self.choices
            ]:
                raise ValidationError(self._format_error(value))
        except TypeError as error:
            raise ValidationError(self._format_error(value)) from error

        return value


def validate_json(value: Union[bytes, bytearray, str]) -> None:
    """
    JSON Validator that can be passed to a Marshmallow `Field`'s validate argument.

    :raises ValidationError: if value is not serializable to JSON
    :param value: an object that should be parseable to JSON
    """
    try:
        utils.validate_json(value)
    except RabbitaiException:
        raise ValidationError("JSON not valid")
