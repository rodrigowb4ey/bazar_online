from collections.abc import AsyncGenerator

import pytest_asyncio
import sqlalchemy as sa
from app.core.models import Base
from app.infra.database import get_session
from app.main import app
from httpx import ASGITransport, AsyncClient
from pydantic_core import MultiHostUrl
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]


@pytest_asyncio.fixture(scope='session')
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """SQLAlchemy DB Engine for testing purposes."""
    with PostgresContainer('postgres:16') as postgres:
        url = MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=postgres.username,
            password=postgres.password,
            host=postgres.get_container_host_ip(),
            port=int(postgres.get_exposed_port(5432)),
            path=postgres.dbname,
        )
        engine = create_async_engine(url=url.unicode_string(), echo=True, future=True)

        async with engine.connect() as conn:
            await conn.execute(sa.text('CREATE SCHEMA IF NOT EXISTS meu_brecho'))
            await conn.commit()

        yield engine

        await engine.dispose()


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """SQLAlchemy DB Session for testing purposes."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Async Test Client using httpx."""

    async def get_session_overrides() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_session] = get_session_overrides
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client

    app.dependency_overrides.clear()
