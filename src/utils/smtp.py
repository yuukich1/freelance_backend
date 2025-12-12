import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import SMTPConfig
from loguru import logger

class SMTPClient(SMTPConfig):

    def send_email(self, to_email: str, subject: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        msg['subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP(self.smtp_host, self.smtp_port, local_hostname='localhost')

        if self.smtp_use_tls:
            server.starttls()

        server.login(self.smtp_user, self.smtp_pass)
        server.sendmail(self.smtp_user, to_email, msg.as_string())
        logger.info(f'Sended email to {to_email}')
        server.quit()

        return True 


