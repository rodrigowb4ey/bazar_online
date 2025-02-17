from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories.user import UserRepository
from app.core.schemas import UserCreate
from app.core.security import create_access_token, verify_password
from app.infra.database import get_session

router = APIRouter()


@router.post('/login', summary='Authenticate user and return access token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[AsyncSession, Depends(get_session)]
) -> dict[str, str]:
    """Authenticate a user with email (as username) and password.

    Returns:
        A dict containing the JWT access token and token type.
    """
    repo = UserRepository(session)
    user = await repo.get_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    hashed_password = str(user.hashed_password)
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register', summary='Register a new user')
async def register(user_in: UserCreate, session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
    """Register a new user and return a JWT token.

    The user details are taken from the request body.
    """
    repo = UserRepository(session)
    existing_user = await repo.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists',
        )
    user = await repo.create(user_in)
    await session.commit()
    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}
