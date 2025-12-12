from datetime import timedelta
import os
from celery import Celery
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from loguru import logger
import sys
from jinja2 import Environment, FileSystemLoader
import os

load_dotenv()

class DatabaseConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./default.db")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

logger.remove()

logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")
logger.add("logs/app.log", rotation="10 MB", level="DEBUG", format="{time} - {level} - {message}")

celery = Celery(
    'email_sender',
    broker=os.getenv('REDIS_BROKER_URL'),
    backend=os.getenv('REDIS_BACKEND_URL')
)

celery.autodiscover_tasks(['src.workers.tasks'])

class SMTPConfig:
    smtp_host = os.getenv('SMTP_HOST', 'smtp.yandex.ru')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER', 'yuukich1')
    smtp_pass = os.getenv('SMTP_PASS', 'password')
    smtp_use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() in ['true', '1', 'yes']


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True
)


def render_email(template_name, **kwargs):
    template = env.get_template(f"/email/{template_name}")
    return template.render(**kwargs)


class SecurityConfig:
    secret_key = os.getenv('SECRET_KEY', 'supersecretkeydefault')
    algorithm = os.getenv('ALGORITHM', 'HS256')
    activation_secret = os.getenv('ACTIVATION_SECRET', 'superactivationsecretdefault')
    exp_activation = timedelta(minutes=30)
    exp = timedelta(hours=2)
    exp_refresh = timedelta(days=7)
    activation_url = os.getenv('ACTIVATION_URL', 'http://localhost:8000/api/auth/activate')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")