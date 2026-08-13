from collections.abc import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker


# Synchronous database configuration.
DATABASE_URL = "sqlite:///./shopping.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# Asynchronous database configuration.
# The +aiosqlite part is required for async SQLite access.
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./shopping.db"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a synchronous database session."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an asynchronous database session."""

    async with AsyncSessionLocal() as session:
        yield session
