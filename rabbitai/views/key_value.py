# -*- coding: utf-8 -*-

import simplejson as json
from flask import request, Response
from flask_appbuilder import expose
from flask_appbuilder.hooks import before_request
from flask_appbuilder.security.decorators import has_access_api
from werkzeug.exceptions import NotFound

from rabbitai import db, event_logger, is_feature_enabled
from rabbitai.models import core as models
from rabbitai.typing import FlaskResponse
from rabbitai.utils import core as utils
from rabbitai.views.base import BaseRabbitaiView, json_error_response


class KV(BaseRabbitaiView):
    """Used for storing and retrieving key value pairs"""

    @staticmethod
    def is_enabled() -> bool:
        return is_feature_enabled("KV_STORE")

    @before_request
    def ensure_enabled(self) -> None:
        if not self.is_enabled():
            raise NotFound()

    @event_logger.log_this
    @has_access_api
    @expose("/store/", methods=["POST"])
    def store(self) -> FlaskResponse:  # pylint: disable=no-self-use
        try:
            value = request.form.get("data")
            obj = models.KeyValue(value=value)
            db.session.add(obj)
            db.session.commit()
        except Exception as ex:  # pylint: disable=broad-except
            return json_error_response(utils.error_msg_from_exception(ex))
        return Response(json.dumps({"id": obj.id}), status=200)

    @event_logger.log_this
    @has_access_api
    @expose("/<int:key_id>/", methods=["GET"])
    def get_value(self, key_id: int) -> FlaskResponse:  # pylint: disable=no-self-use
        try:
            kv = db.session.query(models.KeyValue).filter_by(id=key_id).scalar()
            if not kv:
                return Response(status=404, content_type="text/plain")
        except Exception as ex:  # pylint: disable=broad-except
            return json_error_response(utils.error_msg_from_exception(ex))
        return Response(kv.value, status=200, content_type="text/plain")
