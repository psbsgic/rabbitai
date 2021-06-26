from unittest import mock

from marshmallow import fields, Schema, ValidationError

from rabbitai.databases.schemas import DatabaseParametersSchemaMixin
from rabbitai.db_engine_specs.base import BasicParametersMixin
from rabbitai.models.core import ConfigurationMethod


class DummySchema(Schema, DatabaseParametersSchemaMixin):
    sqlalchemy_uri = fields.String()


class DummyEngine(BasicParametersMixin):
    engine = "dummy"
    default_driver = "dummy"


class InvalidEngine:
    pass


@mock.patch("rabbitai.databases.schemas.get_engine_specs")
def test_database_parameters_schema_mixin(get_engine_specs):
    get_engine_specs.return_value = {"dummy_engine": DummyEngine}
    payload = {
        "engine": "dummy_engine",
        "configuration_method": ConfigurationMethod.DYNAMIC_FORM,
        "parameters": {
            "username": "username",
            "password": "password",
            "host": "localhost",
            "port": 12345,
            "database": "dbname",
        },
    }
    schema = DummySchema()
    result = schema.load(payload)
    assert result == {
        "configuration_method": ConfigurationMethod.DYNAMIC_FORM,
        "sqlalchemy_uri": "dummy+dummy://username:password@localhost:12345/dbname",
    }


def test_database_parameters_schema_mixin_no_engine():
    payload = {
        "configuration_method": ConfigurationMethod.DYNAMIC_FORM,
        "parameters": {
            "username": "username",
            "password": "password",
            "host": "localhost",
            "port": 12345,
            "dbname": "dbname",
        },
    }
    schema = DummySchema()
    try:
        schema.load(payload)
    except ValidationError as err:
        assert err.messages == {
            "_schema": [
                "An engine must be specified when passing individual parameters to a database."
            ]
        }


@mock.patch("rabbitai.databases.schemas.get_engine_specs")
def test_database_parameters_schema_mixin_invalid_engine(get_engine_specs):
    get_engine_specs.return_value = {}
    payload = {
        "engine": "dummy_engine",
        "configuration_method": ConfigurationMethod.DYNAMIC_FORM,
        "parameters": {
            "username": "username",
            "password": "password",
            "host": "localhost",
            "port": 12345,
            "dbname": "dbname",
        },
    }
    schema = DummySchema()
    try:
        schema.load(payload)
    except ValidationError as err:
        assert err.messages == {
            "_schema": ['Engine "dummy_engine" is not a valid engine.']
        }


@mock.patch("rabbitai.databases.schemas.get_engine_specs")
def test_database_parameters_schema_no_mixin(get_engine_specs):
    get_engine_specs.return_value = {"invalid_engine": InvalidEngine}
    payload = {
        "engine": "invalid_engine",
        "configuration_method": ConfigurationMethod.DYNAMIC_FORM,
        "parameters": {
            "username": "username",
            "password": "password",
            "host": "localhost",
            "port": 12345,
            "database": "dbname",
        },
    }
    schema = DummySchema()
    try:
        schema.load(payload)
    except ValidationError as err:
        assert err.messages == {
            "_schema": [
                (
                    'Engine spec "InvalidEngine" does not support '
                    "being configured via individual parameters."
                )
            ]
        }
