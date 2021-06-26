# -*- coding: utf-8 -*-
import json
import logging
from dataclasses import dataclass
from email.utils import make_msgid, parseaddr
from typing import Any, Dict, Optional

from flask_babel import gettext as __

from rabbitai import app
from rabbitai.models.reports import ReportRecipientType
from rabbitai.reports.notifications.base import BaseNotification
from rabbitai.reports.notifications.exceptions import NotificationError
from rabbitai.utils.core import send_email_smtp

logger = logging.getLogger(__name__)


@dataclass
class EmailContent:
    body: str
    data: Optional[Dict[str, Any]] = None
    images: Optional[Dict[str, bytes]] = None


class EmailNotification(BaseNotification):  # pylint: disable=too-few-public-methods
    """
    Sends an email notification for a report recipient
    """

    type = ReportRecipientType.EMAIL

    @staticmethod
    def _get_smtp_domain() -> str:
        return parseaddr(app.config["SMTP_MAIL_FROM"])[1].split("@")[1]

    @staticmethod
    def _error_template(text: str) -> str:
        return __(
            """
            Error: %(text)s
            """,
            text=text,
        )

    def _get_content(self) -> EmailContent:
        if self._content.text:
            return EmailContent(body=self._error_template(self._content.text))
        # Get the domain from the 'From' address ..
        # and make a message id without the < > in the end
        image = None
        csv_data = None
        domain = self._get_smtp_domain()
        msgid = make_msgid(domain)[1:-1]
        body = __(
            """
            <p>%(description)s</p>
            <b><a href="%(url)s">Explore in Rabbitai</a></b><p></p>
            %(img_tag)s
            """,
            description=self._content.description or "",
            url=self._content.url,
            img_tag='<img width="1000px" src="cid:{}">'.format(msgid)
            if self._content.screenshot
            else "",
        )
        if self._content.screenshot:
            image = {msgid: self._content.screenshot}
        if self._content.csv:
            csv_data = {__("%(name)s.csv", name=self._content.name): self._content.csv}
        return EmailContent(body=body, images=image, data=csv_data)

    def _get_subject(self) -> str:
        return __(
            "%(prefix)s %(title)s",
            prefix=app.config["EMAIL_REPORTS_SUBJECT_PREFIX"],
            title=self._content.name,
        )

    def _get_to(self) -> str:
        return json.loads(self._recipient.recipient_config_json)["target"]

    def send(self) -> None:
        subject = self._get_subject()
        content = self._get_content()
        to = self._get_to()
        try:
            send_email_smtp(
                to,
                subject,
                content.body,
                app.config,
                files=[],
                data=content.data,
                images=content.images,
                bcc="",
                mime_subtype="related",
                dryrun=False,
            )
            logger.info("Report sent to email")
        except Exception as ex:
            raise NotificationError(ex)
