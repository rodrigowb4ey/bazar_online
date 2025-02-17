from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.repositories.user import UserRepository
from app.core.security import decode_access_token
from app.infra.database import get_session

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/v1/auth/login')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    """Validate the JWT token and return the current user.

    Args:
        token: JWT token from the Authorization header.
        session: Async SQLAlchemy session.

    Returns:
        The authenticated user.
    """
    payload: dict[str, Any] | None = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )
    user_id = payload.get('sub')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )
    repo = UserRepository(session)
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
        )
    return user
