import smtplib

from nepse_tools.share_market.notifiers.base_notifier import BaseNotifier
from nepse_tools.share_market.notifiers.ma_cross_notifier import MACrossNotifier
from nepse_tools.utils.notification_mediums.email import EmailManager


class BulkNotifier:
    def __init__(self, notifiers: list[BaseNotifier]):
        self._messages = {}
        self.notifiers: list[BaseNotifier] = []

        self.email_manager: EmailManager = EmailManager()

        self.add_notifiers(notifiers)

    def add_notifiers(self, notifiers: list[BaseNotifier]):
        self.notifiers += notifiers

        for notifier in notifiers:
            for email in notifier.notification_emails:
                if email not in self._messages:
                    self._messages[email] = []

    def run(self):
        for notifier in self.notifiers:
            notifier_output = notifier.run(send_email=False)

            if notifier_output is not None:
                for email in notifier.notification_emails:
                    self._messages[email].append(notifier_output)

        self.send_email()

    def send_email(self):
        with smtplib.SMTP_SSL(
                self.email_manager.smtp_server_address,
                self.email_manager.smtp_server_port,
                context=self.email_manager.email_context
        ) as server:
            for email, email_data in self._messages.items():
                if email_data:
                    self.email_manager.send_email(
                        subject=" || ".join([data["subject"] for data in email_data]),
                        plain_message="\n\n".join(data["plain_message"] for data in email_data),
                        html_message="<hr><hr>".join(data["html_message"] for data in email_data),
                        receiver_email=email,
                        server=server
                    )
