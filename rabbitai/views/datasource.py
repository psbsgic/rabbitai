import json
from collections import Counter

from flask import request
from flask_appbuilder import expose
from flask_appbuilder.security.decorators import has_access_api
from flask_babel import _

from rabbitai import app, db, event_logger
from rabbitai.connectors.connector_registry import ConnectorRegistry
from rabbitai.datasets.commands.exceptions import DatasetForbiddenError
from rabbitai.exceptions import RabbitaiException, RabbitaiSecurityException
from rabbitai.typing import FlaskResponse
from rabbitai.views.base import check_ownership

from .base import api, BaseRabbitaiView, handle_api_exception, json_error_response


class Datasource(BaseRabbitaiView):
    """数据源视图。"""

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
        """
        从数据源系统获取列信息。

        :param datasource_type: 数据源类型。
        :param datasource_id: 数据源标识。
        :return:
        """

        datasource = ConnectorRegistry.get_datasource(datasource_type, datasource_id, db.session)
        try:
            external_metadata = datasource.external_metadata()
        except RabbitaiException as ex:
            return json_error_response(str(ex), status=400)
        return self.json_response(external_metadata)
