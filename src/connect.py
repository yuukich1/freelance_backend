from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from src.config import DatabaseConfig

async_engine = create_async_engine(DatabaseConfig.DATABASE_URL, echo=False)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

sync_engine = create_engine(DatabaseConfig.SYNC_DATABASE_URL, echo=False)
SyncSession = sessionmaker(bind=sync_engine)