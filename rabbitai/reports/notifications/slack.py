# -*- coding: utf-8 -*-
import json
import logging
from io import IOBase
from typing import Optional, Union

from flask_babel import gettext as __
from retry.api import retry
from slack import WebClient
from slack.errors import SlackApiError, SlackClientError

from rabbitai import app
from rabbitai.models.reports import ReportRecipientType
from rabbitai.reports.notifications.base import BaseNotification
from rabbitai.reports.notifications.exceptions import NotificationError

logger = logging.getLogger(__name__)


class SlackNotification(BaseNotification):  # pylint: disable=too-few-public-methods
    """
    Sends a slack notification for a report recipient
    """

    type = ReportRecipientType.SLACK

    def _get_channel(self) -> str:
        return json.loads(self._recipient.recipient_config_json)["target"]

    @staticmethod
    def _error_template(name: str, description: str, text: str) -> str:
        return __(
            """
            *%(name)s*\n
            %(description)s\n
            Error: %(text)s
            """,
            name=name,
            description=description,
            text=text,
        )

    def _get_body(self) -> str:
        if self._content.text:
            return self._error_template(
                self._content.name, self._content.description or "", self._content.text
            )
        return __(
            """
            *%(name)s*\n
            %(description)s\n
            <%(url)s|Explore in Rabbitai>
            """,
            name=self._content.name,
            description=self._content.description or "",
            url=self._content.url,
        )

    def _get_inline_file(self) -> Optional[Union[str, IOBase, bytes]]:
        if self._content.csv:
            return self._content.csv
        if self._content.screenshot:
            return self._content.screenshot
        return None

    @retry(SlackApiError, delay=10, backoff=2, tries=5)
    def send(self) -> None:
        file = self._get_inline_file()
        title = self._content.name
        channel = self._get_channel()
        body = self._get_body()
        file_type = "csv" if self._content.csv else "png"
        try:
            token = app.config["SLACK_API_TOKEN"]
            if callable(token):
                token = token()
            client = WebClient(token=token, proxy=app.config["SLACK_PROXY"])
            # files_upload returns SlackResponse as we run it in sync mode.
            if file:
                client.files_upload(
                    channels=channel,
                    file=file,
                    initial_comment=body,
                    title=title,
                    filetype=file_type,
                )
            else:
                client.chat_postMessage(channel=channel, text=body)
            logger.info("Report sent to slack")
        except SlackClientError as ex:
            raise NotificationError(ex)
