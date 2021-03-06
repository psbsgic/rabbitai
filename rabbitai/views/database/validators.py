# -*- coding: utf-8 -*-

from typing import Optional, Type

from flask_babel import lazy_gettext as _
from marshmallow import ValidationError
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError

from rabbitai import security_manager
from rabbitai.models.core import Database


def sqlalchemy_uri_validator(
    uri: str, exception: Type[ValidationError] = ValidationError
) -> None:
    """
    Check if a user has submitted a valid SQLAlchemy URI
    """
    try:
        make_url(uri.strip())
    except (ArgumentError, AttributeError):
        raise exception(
            [
                _(
                    "Invalid connection string, a valid string usually follows:"
                    "'DRIVER://USER:PASSWORD@DB-HOST/DATABASE-NAME'"
                    "<p>"
                    "Example:'postgresql://user:password@your-postgres-db/database'"
                    "</p>"
                )
            ]
        )


def schema_allows_csv_upload(database: Database, schema: Optional[str]) -> bool:
    if not database.allow_csv_upload:
        return False
    schemas = database.get_schema_access_for_csv_upload()
    if schemas:
        return schema in schemas
    return security_manager.can_access_database(database)
