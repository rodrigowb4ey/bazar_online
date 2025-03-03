import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.infra.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events.

    Args:
        _app: The FastAPI application instance.

    Yields:
        None
    """
    logger.info('Starting up the Bazar Online API...')
    yield
    await engine.dispose()
    logger.info('Shutting down the Bazar Online API...')


app = FastAPI(
    title='Bazar Online API',
    description='API for the Bazar Online application.',
    version='0.1.0',
    lifespan=lifespan,
)


@app.get('/healthcheck', response_model=dict, tags=['Healthcheck'])
def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint.

    Returns:
        A dictionary containing the application's health status.
    """
    return {'status': 'ok'}


app.include_router(api_v1_router, prefix='/v1')
