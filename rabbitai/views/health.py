# -*- coding: utf-8 -*-

from rabbitai import app, talisman
from rabbitai.typing import FlaskResponse


@talisman(force_https=False)
@app.route("/ping")
def ping() -> FlaskResponse:
    return "OK"


@talisman(force_https=False)
@app.route("/healthcheck")
def healthcheck() -> FlaskResponse:
    return "OK"


@talisman(force_https=False)
@app.route("/health")
def health() -> FlaskResponse:
    return "OK"
