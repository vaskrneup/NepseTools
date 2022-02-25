import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config


class EmailManager:
    def __init__(self):
        self._sender_email: str = config("MAIL_EMAIL")
        self._mail_password: str = config("MAIL_PASSWORD")
        self._smtp_server_address: str = config("MAIL_SMTP_SERVER_ADDRESS")
        self._smtp_server_port: int = int(config("MAIL_SMTP_SERVER_PORT"))

        self._email_session: smtplib.SMTP_SSL | None = None

    @staticmethod
    def attach_documents_to_email(message: MIMEMultipart, attachment_file_paths: list[str]):
        for attachment_file_path in attachment_file_paths:
            with open(attachment_file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_file_path)}",
            )
            message.attach(part)

    def send_email(
            self,
            subject: str,
            plain_message: str,
            receiver_emails: list[str],
            html_message: str = None,
            attachment_file_paths: list[str] = None
    ) -> bool:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
                self._smtp_server_address,
                self._smtp_server_port,
                context=context
        ) as server:
            server.login(self._sender_email, self._mail_password)

            for receiver_email in receiver_emails:
                message = MIMEMultipart("alternative")

                if attachment_file_paths is not None:
                    self.attach_documents_to_email(message, attachment_file_paths)

                message["Subject"] = subject
                message["From"] = self._sender_email
                message["To"] = receiver_email
                message["Bcc"] = receiver_email

                message.attach(MIMEText(plain_message, "plain"))
                if html_message:
                    # Second one will try to render first in client side.
                    message.attach(MIMEText(html_message, "html"))

                server.sendmail(
                    self._sender_email, receiver_email, message.as_string()
                )

        return True
