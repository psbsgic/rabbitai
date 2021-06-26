# -*- coding: utf-8 -*-
from rabbitai.models.reports import ReportRecipients
from rabbitai.reports.notifications.base import BaseNotification, NotificationContent
from rabbitai.reports.notifications.email import EmailNotification
from rabbitai.reports.notifications.slack import SlackNotification


def create_notification(
    recipient: ReportRecipients, notification_content: NotificationContent
) -> BaseNotification:
    """
    Notification polymorphic factory
    Returns the Notification class for the recipient type
    """
    for plugin in BaseNotification.plugins:
        if plugin.type == recipient.type:
            return plugin(recipient, notification_content)
    raise Exception("Recipient type not supported")
