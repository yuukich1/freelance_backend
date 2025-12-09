import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import SMTPConfig
from loguru import logger

class SMTPClient(SMTPConfig):

    def send_email(self, to_email: str, subject: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.SMTP_USER
        msg['To'] = to_email
        msg['subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT, local_hostname='localhost')

        if self.SMTP_USE_TLS:
            server.starttls()

        server.login(self.SMTP_USER, self.SMTP_PASS)
        server.sendmail(self.SMTP_USER, to_email, msg.as_string())
        logger.info(f'Sended email to {to_email}')
        server.quit()

        return True 


