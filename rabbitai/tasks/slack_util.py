"""
DEPRECATION NOTICE: this module is deprecated and will be removed on 2.0.
"""
import logging
from io import IOBase
from typing import cast, Optional, Union

from flask import current_app
from retry.api import retry
from slack import WebClient
from slack.errors import SlackApiError
from slack.web.slack_response import SlackResponse

# Globals
logger = logging.getLogger("tasks.slack_util")


@retry(SlackApiError, delay=10, backoff=2, tries=5)
def deliver_slack_msg(
    slack_channel: str,
    subject: str,
    body: str,
    file: Optional[Union[str, IOBase, bytes]],
) -> None:
    config = current_app.config
    token = config["SLACK_API_TOKEN"]
    if callable(token):
        token = token()
    client = WebClient(token=token, proxy=config["SLACK_PROXY"])
    # files_upload returns SlackResponse as we run it in sync mode.
    if file:
        response = cast(
            SlackResponse,
            client.files_upload(
                channels=slack_channel, file=file, initial_comment=body, title=subject
            ),
        )
        assert response["file"], str(response)  # the uploaded file
    else:
        response = cast(
            SlackResponse, client.chat_postMessage(channel=slack_channel, text=body),
        )
        assert response["message"]["text"], str(response)
    logger.info("Sent the report to the slack %s", slack_channel)
