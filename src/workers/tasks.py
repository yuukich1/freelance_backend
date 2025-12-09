from src.config import celery, render_email
from src.utils.smtp import SMTPClient
from loguru import logger

@celery.task
def send_welcome_email_task(to_email, username: str, action_url: str):
    html = render_email('welcome.html', username=username, action_url=action_url)
    SMTPClient().send_email(to_email=to_email, subject='Welcome', message=html)
    return True

    
