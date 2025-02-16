from collections.abc import AsyncGenerator

import pytest_asyncio
from app.core.models import Base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL: str = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture(scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """SQLAlchemy DB Engine for testing purposes."""
    engine: AsyncEngine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={'check_same_thread': False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """SQLAlchemy DB Session for testing purposes."""
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
