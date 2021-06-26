import logging
from typing import Optional

from flask import flash, request, Response
from flask_appbuilder import expose
from flask_appbuilder.security.decorators import has_access_api
from werkzeug.utils import redirect

from rabbitai import db, event_logger
from rabbitai.models import core as models
from rabbitai.typing import FlaskResponse
from rabbitai.views.base import BaseRabbitaiView

logger = logging.getLogger(__name__)


class R(BaseRabbitaiView):
    """used for short urls"""

    @staticmethod
    def _validate_url(url: Optional[str] = None) -> bool:
        if url and (
            url.startswith("//rabbitai/dashboard/")
            or url.startswith("//rabbitai/explore/")
        ):
            return True
        return False

    @event_logger.log_this
    @expose("/<int:url_id>")
    def index(self, url_id: int) -> FlaskResponse:
        url = db.session.query(models.Url).get(url_id)
        if url and url.url:
            explore_url = "//rabbitai/explore/?"
            if url.url.startswith(explore_url):
                explore_url += f"r={url_id}"
                return redirect(explore_url[1:])
            if self._validate_url(url.url):
                return redirect(url.url[1:])
            return redirect("/")

        flash("URL to nowhere...", "danger")
        return redirect("/")

    @event_logger.log_this
    @has_access_api
    @expose("/shortner/", methods=["POST"])
    def shortner(self) -> FlaskResponse:
        url = request.form.get("data")
        if not self._validate_url(url):
            logger.warning("Invalid URL: %s", url)
            return Response(f"Invalid URL: {url}", 400)
        obj = models.Url(url=url)
        db.session.add(obj)
        db.session.commit()
        return Response(
            "{scheme}://{request.headers[Host]}/r/{obj.id}".format(
                scheme=request.scheme, request=request, obj=obj
            ),
            mimetype="text/plain",
        )
