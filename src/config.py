import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from loguru import logger
import sys

load_dotenv()

class DatabaseConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./default.db")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

logger.remove()

logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")
logger.add("logs/app.log", rotation="10 MB", level="DEBUG", format="{time} - {level} - {message}")
