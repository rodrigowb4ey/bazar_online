from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

engine = create_async_engine(
    url=settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields an async SQLAlchemy session."""
    async with AsyncSessionFactory() as session:
        yield session


T_DbSession = Annotated[AsyncSession, Depends(get_session)]
