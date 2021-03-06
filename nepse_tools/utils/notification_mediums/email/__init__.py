"""
Module to provide initial functionality for sending emails.
"""

import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config


class EmailManager:
    """
    Base Class to provide basic emailing functionality.
    """

    def __init__(self):
        self._sender_email: str = config("MAIL_EMAIL")
        self._mail_password: str = config("MAIL_PASSWORD")

        self.smtp_server_address: str = config("MAIL_SMTP_SERVER_ADDRESS")
        self.smtp_server_port: int = int(config("MAIL_SMTP_SERVER_PORT"))
        self.email_context = ssl.create_default_context()

    @staticmethod
    def get_send_mail_kwargs(
            subject: str,
            plain_message: str,
            html_message: str,
            receiver_emails: list[str],
            attachment_file_paths: list[str] = None,
    ) -> dict:
        """
        Provides a dictionary of parameters accepted by `EmailManager.send_email` method.

        Args:
            subject: Subject of the mail
            plain_message: Plain Text form of email body
            html_message: HTML form of email body
            receiver_emails: List of emails of the receivers'
            attachment_file_paths: File paths to the email file attachments

        Returns:
            Dictionary that is accepted by `EmailManager.send_email` method.

        """
        return {
            "subject": subject,
            "plain_message": plain_message,
            "html_message": html_message,
            "receiver_emails": receiver_emails,
            "attachment_file_paths": attachment_file_paths
        }

    @staticmethod
    def attach_documents_to_email(message: MIMEMultipart, attachment_file_paths: list[str]) -> None:
        """
        Attaches the files provided to the message.

        Args:
            message: Message Object to which the files must be attached
            attachment_file_paths: Paths to the file which must be attached to the message

        Returns:
            None

        """
        for attachment_file_path in attachment_file_paths:
            with open(attachment_file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_file_path)}",
            )
            part.add_header(
                "Content-ID",
                f'<{os.path.basename(attachment_file_path).replace(".", "_").strip()}>'
            )
            message.attach(part)

    def _send_email(
            self,
            subject: str,
            plain_message: str,
            receiver_email: list[str],
            html_message: str = None,
            attachment_file_paths: list[str] = None,
            server: smtplib.SMTP_SSL = None,
    ) -> None:
        """
        Internal method to send email.

        Args:
            subject: Subject of the mail
            plain_message: Plain Text form of email body
            html_message: HTML form of email body
            receiver_email: List of emails of the receivers'
            attachment_file_paths: File paths to the email file attachments
            server: Server|Connection that will be used to send email

        Returns:
            None

        """
        server.login(self._sender_email, self._mail_password)

        message = MIMEMultipart("alternative")

        if attachment_file_paths is not None:
            self.attach_documents_to_email(message, attachment_file_paths)

        message["Subject"] = subject
        message["From"] = self._sender_email
        message["To"] = ",".join(receiver_email)

        message.attach(MIMEText(plain_message, "plain"))
        if html_message:
            # Second one will try to render first in client side.
            message.attach(MIMEText(html_message, "html"))

        server.sendmail(
            self._sender_email, receiver_email, message.as_string()
        )

    def send_email(
            self,
            subject: str,
            plain_message: str,
            receiver_email: str | list[str],
            html_message: str = None,
            attachment_file_paths: list[str] = None,
            server: smtplib.SMTP_SSL = None
    ) -> bool:
        """
        Sends email using given parameters.

        Args:
            subject: Subject of the mail
            plain_message: Plain Text form of email body
            html_message: HTML form of email body
            receiver_email: List of emails of the receivers'
            attachment_file_paths: File paths to the email file attachments
            server: Server|Connection that will be used to send email

        Returns:
            None

        """
        if type(receiver_email) is str:
            receiver_email = [receiver_email]

        if server is None:
            with smtplib.SMTP_SSL(
                    self.smtp_server_address,
                    self.smtp_server_port,
                    context=self.email_context
            ) as server:
                self._send_email(
                    subject,
                    plain_message,
                    receiver_email,
                    html_message,
                    attachment_file_paths,
                    server
                )
        else:
            self._send_email(
                subject,
                plain_message,
                receiver_email,
                html_message,
                attachment_file_paths,
                server
            )

        return True
