import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from scr.utils import read_config, read_message_text
from scr.constants import MAIL_SERVERS

class SMTPSender:
    def __init__(self):
        self.sender, self.password, self.recipients, self.subject, self.attachments = read_config()
        self.mail_server = MAIL_SERVERS[self.sender.split('@')[1]]

    def send(self):
        try:
            client = smtplib.SMTP_SSL(*self.mail_server)
            client.login(self.sender, self.password)
            message = self.build_message()
            client.sendmail(self.sender, self.recipients, message)
            client.quit()
            print('Email delivered successfully!')
        except smtplib.SMTPRecipientsRefused:
            print('Invalid recipient address.')
        except smtplib.SMTPAuthenticationError:
            print('Authentication error.')
        except smtplib.SMTPSenderRefused:
            print('Sender address refused.')
        except smtplib.SMTPConnectError:
            print('Connection error.')
        except smtplib.SMTPException as e:
            print('SMTP error:', e)

    def build_message(self) -> str:
        msg = MIMEMultipart("mixed") if self.attachments else MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg["To"] = ",".join(self.recipients)

        alternative = MIMEMultipart("alternative")
        alternative.attach(MIMEText(read_message_text(), "plain"))
        msg.attach(alternative)

        self.add_attachments(msg)
        return msg.as_string()

    def add_attachments(self, msg):
        for filename in self.attachments:
            with open(f'files/attachments/{filename}', 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header("Content-Disposition", "attachment", filename=filename)
                msg.attach(part)
