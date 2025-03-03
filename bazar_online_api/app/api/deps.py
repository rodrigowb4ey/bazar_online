from typing import Annotated

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.models import User
from app.core.security import T_Token
from app.core.settings import settings
from app.infra.database import T_DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/login')


async def get_current_user(token: T_Token, session: T_DbSession) -> User:
    """Validate the JWT token and return the current user.

    Args:
        token: JWT token from the Authorization header.
        session: Async SQLAlchemy session.

    Returns:
        The authenticated user.
    """
    try:
        payload = jwt.decode(token, algorithms=[settings.ACCESS_TOKEN_ALGORITHM], key=settings.SECRET_KEY)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        ) from None

    email: str = payload.get('sub', '')
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )

    user = await session.scalar(sa.select(User).where(User.email == email))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )

    return user


T_CurrentUser = Annotated[User, Depends(get_current_user)]
