import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config


class BaseNotifier:
    def send_email(self, subject: str, receiver_emails: list[str], attachment_file_path: str = None):
        sender_email = config("MAIL_EMAIL")

        # Create the plain-text and HTML version of your message
        text = """\
         Hi,
         How are you?
         Real Python has many great tutorials:
         www.realpython.com"""
        html = """\
         <html>
           <body>
             <p>Hi,<br>
                How are you?<br>
                <a href="https://www.realpython.com">Real Python</a> 
                has many great tutorials.
             </p>
           </body>
         </html>
         """

        # Create secure connection with server and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
                config("MAIL_SMTP_SERVER_ADDRESS"),
                int(config("MAIL_SMTP_SERVER_PORT")),
                context=context
        ) as server:
            server.login(sender_email, config("MAIL_PASSWORD"))

            for receiver_email in receiver_emails:
                message = MIMEMultipart("alternative")

                if attachment_file_path is not None:
                    with open(attachment_file_path, "rb") as attachment:
                        # Add file as application/octet-stream
                        # Email client can usually download this automatically as attachment
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment_file_path)}",
                    )
                    message.attach(part)

                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Bcc"] = receiver_email  # Recommended for mass emails

                # Turn these into plain/html MIMEText objects
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)

                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
