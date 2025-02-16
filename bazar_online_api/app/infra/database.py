from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = 'sqlite+aiosqlite:///./sqlite.db'

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields an async SQLAlchemy session."""
    async with async_session_maker() as session:
        yield session
