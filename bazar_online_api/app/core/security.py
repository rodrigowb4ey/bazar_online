from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/login')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the given password."""
    return pwd_context.hash(password)


def create_access_token(email: str) -> str:
    """Create a JWT access token.

    Args:
        email: User e-mail.

    Returns:
        A JWT encoded access token.
    """
    return jwt.encode(
        {'sub': email, 'exp': datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)},
        algorithm=settings.ACCESS_TOKEN_ALGORITHM,
        key=settings.SECRET_KEY,
    )


T_Token = Annotated[str, Depends(oauth2_scheme)]
