from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from app.core.models import Base
from app.infra.database import get_session
from app.main import app
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
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with async_session(bind=connection) as session:
            yield session
        await transaction.rollback()


@pytest.fixture(autouse=True)
def override_get_session(session: AsyncSession) -> Generator[None, None, None]:
    """Automatically override the get_session dependency for the FastAPI app.
    with the test session provided by the 'session' fixture.
    """  # noqa: D205
    app.dependency_overrides[get_session] = lambda: session
    yield
    app.dependency_overrides.pop(get_session, None)
