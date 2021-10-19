# -*- coding: utf-8 -*-
import json
import logging
from io import IOBase
from typing import Optional, Union

import backoff
from flask_babel import gettext as __
from slack import WebClient
from slack.errors import SlackApiError, SlackClientError
from tabulate import tabulate

from rabbitai import app
from rabbitai.models.reports import ReportRecipientType
from rabbitai.reports.notifications.base import BaseNotification
from rabbitai.reports.notifications.exceptions import NotificationError

logger = logging.getLogger(__name__)

# Slack only allows Markdown messages up to 4k chars
MAXIMUM_MESSAGE_SIZE = 4000


class SlackNotification(BaseNotification):  # pylint: disable=too-few-public-methods
    """
    Sends a slack notification for a report recipient
    """

    type = ReportRecipientType.SLACK

    def _get_channel(self) -> str:
        return json.loads(self._recipient.recipient_config_json)["target"]

    def _message_template(self, table: str = "") -> str:
        return __(
            """*%(name)s*

%(description)s

<%(url)s|Explore in Rabbitai>

%(table)s
""",
            name=self._content.name,
            description=self._content.description or "",
            url=self._content.url,
            table=table,
        )

    @staticmethod
    def _error_template(name: str, description: str, text: str) -> str:
        return __(
            """*%(name)s*

%(description)s

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

        if self._content.embedded_data is None:
            return self._message_template()

        # Embed data in the message
        df = self._content.embedded_data

        # Slack Markdown only works on messages shorter than 4k chars, so we might
        # need to truncate the data
        for i in range(len(df) - 1):
            truncated_df = df[: i + 1].fillna("")
            truncated_df = truncated_df.append(
                {k: "..." for k in df.columns}, ignore_index=True
            )
            tabulated = tabulate(truncated_df, headers="keys", showindex=False)
            table = f"```\n{tabulated}\n```\n\n(table was truncated)"
            message = self._message_template(table)
            if len(message) > MAXIMUM_MESSAGE_SIZE:
                # Decrement i and build a message that is under the limit
                truncated_df = df[:i].fillna("")
                truncated_df = truncated_df.append(
                    {k: "..." for k in df.columns}, ignore_index=True
                )
                tabulated = tabulate(truncated_df, headers="keys", showindex=False)
                table = (
                    f"```\n{tabulated}\n```\n\n(table was truncated)"
                    if len(truncated_df) > 0
                    else ""
                )
                break

        # Send full data
        else:
            tabulated = tabulate(df, headers="keys", showindex=False)
            table = f"```\n{tabulated}\n```"

        return self._message_template(table)

    def _get_inline_file(self) -> Optional[Union[str, IOBase, bytes]]:
        if self._content.csv:
            return self._content.csv
        if self._content.screenshot:
            return self._content.screenshot
        return None

    @backoff.on_exception(backoff.expo, SlackApiError, factor=10, base=2, max_tries=5)
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
