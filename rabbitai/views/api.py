# -*- coding: utf-8 -*-

from typing import Any

import simplejson as json
from flask import request
from flask_appbuilder import expose
from flask_appbuilder.api import rison
from flask_appbuilder.security.decorators import has_access_api

from rabbitai import db, event_logger
from rabbitai.charts.commands.exceptions import (
    TimeRangeAmbiguousError,
    TimeRangeParseFailError,
)
from rabbitai.common.query_context import QueryContext
from rabbitai.legacy import update_time_range
from rabbitai.models.slice import Slice
from rabbitai.typing import FlaskResponse
from rabbitai.utils import core as utils
from rabbitai.utils.date_parser import get_since_until
from rabbitai.views.base import api, BaseRabbitaiView, handle_api_exception

get_time_range_schema = {"type": "string"}


class Api(BaseRabbitaiView):
    """API访问视图。

    /v1/query/

    /v1/form_data/

    /v1/time_range/
    """

    @event_logger.log_this
    @api
    @handle_api_exception
    @has_access_api
    @expose("/v1/query/", methods=["POST"])
    def query(self) -> FlaskResponse:
        """
        Takes a query_obj constructed in the client and returns payload data response
        for the given query_obj.

        raises RabbitaiSecurityException: If the user cannot access the resource
        """

        query_context = QueryContext(**json.loads(request.form["query_context"]))
        query_context.raise_for_access()
        result = query_context.get_payload()
        payload_json = result["queries"]
        return json.dumps(
            payload_json, default=utils.json_int_dttm_ser, ignore_nan=True
        )

    @event_logger.log_this
    @api
    @handle_api_exception
    @has_access_api
    @expose("/v1/form_data/", methods=["GET"])
    def query_form_data(self) -> FlaskResponse:
        """
        Get the formdata stored in the database for existing slice.
        params: slice_id: integer
        """

        form_data = {}
        slice_id = request.args.get("slice_id")
        if slice_id:
            slc = db.session.query(Slice).filter_by(id=slice_id).one_or_none()
            if slc:
                form_data = slc.form_data.copy()

        update_time_range(form_data)

        return json.dumps(form_data)

    @api
    @handle_api_exception
    @has_access_api
    @rison(get_time_range_schema)
    @expose("/v1/time_range/", methods=["GET"])
    def time_range(self, **kwargs: Any) -> FlaskResponse:
        """Get actually time range from human readable string or datetime expression"""

        time_range = kwargs["rison"]
        try:
            since, until = get_since_until(time_range)
            result = {
                "since": since.isoformat() if since else "",
                "until": until.isoformat() if until else "",
                "timeRange": time_range,
            }
            return self.json_response({"result": result})
        except (ValueError, TimeRangeParseFailError, TimeRangeAmbiguousError) as error:
            error_msg = {"message": f"Unexpected time range: {error}"}
            return self.json_response(error_msg, 400)
