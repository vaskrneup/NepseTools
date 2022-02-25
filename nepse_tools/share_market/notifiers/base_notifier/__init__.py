import jinja2

from nepse_tools.utils.notification_mediums.email import EmailManager


class BaseNotifier:
    def __init__(self):
        self.email_manager = EmailManager()

    @staticmethod
    def create_message_from_template(template_path: str, template_data: dict):
        with open(template_path, "r") as template_file:
            template = jinja2.Template(template_file.read())
            template.render(**template_data)

    def send_email(
            self,
            subject: str,
            plain_message: str,
            receiver_emails: list[str],
            html_message: str = None,
            attachment_file_paths: list[str] = None
    ):
        return self.email_manager.send_email(
            subject=subject,
            plain_message=plain_message,
            receiver_emails=receiver_emails,
            html_message=html_message,
            attachment_file_paths=attachment_file_paths
        )
