# -*- coding: utf-8 -*-

import json
from collections import Counter

from flask import request
from flask_appbuilder import expose
from flask_appbuilder.security.decorators import has_access_api
from flask_babel import _

from rabbitai import app, db, event_logger
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.connectors.sqla.utils import get_physical_table_metadata
from rabbitai.datasets.commands.exceptions import DatasetForbiddenError
from rabbitai.exceptions import RabbitaiException, RabbitaiSecurityException
from rabbitai.models.core import Database
from rabbitai.typing import FlaskResponse
from rabbitai.views.base import check_ownership

from ..utils.core import parse_js_uri_path_item
from .base import api, BaseRabbitaiView, handle_api_exception, json_error_response


class Datasource(BaseRabbitaiView):
    """数据源模型视图。"""

    @expose("/save/", methods=["POST"])
    @event_logger.log_this_with_context(
        action=lambda self, *args, **kwargs: f"{self.__class__.__name__}.save",
        log_to_statsd=False,
    )
    @has_access_api
    @api
    @handle_api_exception
    def save(self) -> FlaskResponse:
        data = request.form.get("data")
        if not isinstance(data, str):
            return json_error_response(_("Request missing data field."), status=500)

        datasource_dict = json.loads(data)
        datasource_id = datasource_dict.get("id")
        datasource_type = datasource_dict.get("type")
        database_id = datasource_dict["database"].get("id")
        orm_datasource = ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
        orm_datasource.database_id = database_id

        if "owners" in datasource_dict and orm_datasource.owner_class is not None:
            # Check ownership
            if app.config["OLD_API_CHECK_DATASET_OWNERSHIP"]:
                try:
                    check_ownership(orm_datasource)
                except RabbitaiSecurityException:
                    raise DatasetForbiddenError()

            datasource_dict["owners"] = (
                db.session.query(orm_datasource.owner_class)
                .filter(orm_datasource.owner_class.id.in_(datasource_dict["owners"]))
                .all()
            )

        duplicates = [
            name
            for name, count in Counter(
                [col["column_name"] for col in datasource_dict["columns"]]
            ).items()
            if count > 1
        ]
        if duplicates:
            return json_error_response(
                _(
                    "Duplicate column name(s): %(columns)s",
                    columns=",".join(duplicates),
                ),
                status=409,
            )
        orm_datasource.update_from_object(datasource_dict)
        data = orm_datasource.data
        db.session.commit()

        return self.json_response(data)

    @expose("/get/<datasource_type>/<datasource_id>/")
    @has_access_api
    @api
    @handle_api_exception
    def get(self, datasource_type: str, datasource_id: int) -> FlaskResponse:
        datasource = ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
        return self.json_response(datasource.data)

    @expose("/external_metadata/<datasource_type>/<datasource_id>/")
    @has_access_api
    @api
    @handle_api_exception
    def external_metadata(self, datasource_type: str, datasource_id: int) -> FlaskResponse:
        """Gets column info from the source system"""

        datasource = ConnectorRegistry.get_datasource(
            datasource_type, datasource_id, db.session
        )
        try:
            external_metadata = datasource.external_metadata()
        except RabbitaiException as ex:
            return json_error_response(str(ex), status=400)
        return self.json_response(external_metadata)

    @expose(
        "/external_metadata_by_name/<datasource_type>/<database_name>/"
        "<schema_name>/<table_name>/"
    )
    @has_access_api
    @api
    @handle_api_exception
    def external_metadata_by_name(
        self,
        datasource_type: str,
        database_name: str,
        schema_name: str,
        table_name: str,
    ) -> FlaskResponse:
        """Gets table metadata from the source system and SQLAlchemy inspector"""

        database_name = parse_js_uri_path_item(database_name) or ""
        schema_name = parse_js_uri_path_item(schema_name, eval_undefined=True) or ""
        table_name = parse_js_uri_path_item(table_name) or ""

        datasource = ConnectorRegistry.get_datasource_by_name(
            session=db.session,
            datasource_type=datasource_type,
            database_name=database_name,
            schema=schema_name,
            datasource_name=table_name,
        )
        try:
            if datasource is not None:
                external_metadata = datasource.external_metadata()
            else:
                # Use the SQLAlchemy inspector to get columns
                database = (
                    db.session.query(Database)
                    .filter_by(database_name=database_name)
                    .one()
                )
                external_metadata = get_physical_table_metadata(
                    database=database, table_name=table_name, schema_name=schema_name,
                )
        except RabbitaiException as ex:
            return json_error_response(str(ex), status=400)
        return self.json_response(external_metadata)
