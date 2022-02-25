import jinja2
import pandas as pd
from decouple import config

from nepse_tools.utils.notification_mediums.email import EmailManager


class BaseNotifier:
    def __init__(
            self,
            scripts: list[str],
            notification_emails: list[str] = None,
            share_price_data_csv_path: str = config("SHARE_PRICE_STORAGE_LOCATION")
    ):
        self.scripts = scripts
        self.email_manager: EmailManager = EmailManager()
        self.share_price_df = pd.read_csv(share_price_data_csv_path)

        self.notification_emails = notification_emails

    @staticmethod
    def create_message_from_template(template_path: str, template_data: dict):
        with open(template_path, "r") as template_file:
            template = jinja2.Template(template_file.read())
            template.render(**template_data)

    def process_data(self, email: str = None, *args, **kwargs) -> dict | None:
        raise NotImplementedError()

    def send_email(
            self,
            subject: str,
            plain_message: str,
            receiver_emails: list[str],
            html_message: str = None,
            attachment_file_paths: list[str] = None,
    ):
        return self.email_manager.send_email(
            subject=subject,
            plain_message=plain_message,
            receiver_email=receiver_emails,
            html_message=f"<html><body>{html_message}</html></body>" if html_message else None,
            attachment_file_paths=attachment_file_paths
        )

    def run(self, send_email: bool = True, has_dynamic_user_content: bool = False) -> None | dict:
        if has_dynamic_user_content:
            dynamic_message_dict = {}

            for email in self.notification_emails:
                processed_data = self.process_data(email)

                if processed_data is None:
                    return None

                if send_email:
                    self.send_email(**processed_data)

                dynamic_message_dict[email] = processed_data

            return dynamic_message_dict
        else:
            processed_data = self.process_data()

            if processed_data is None:
                return None

            if send_email:
                self.send_email(**processed_data)

            return processed_data
