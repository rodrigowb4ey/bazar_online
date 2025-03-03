from http import HTTPStatus
from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import T_CurrentUser
from app.core.models import User
from app.core.schemas import Token, UserCreate
from app.core.security import create_access_token, verify_password
from app.infra.database import T_DbSession

router = APIRouter()

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/login', summary='Authenticate user and return access token', status_code=HTTPStatus.OK)
async def login(form_data: T_OAuth2Form, session: T_DbSession) -> Token:
    """Authenticate a user with email (as username) and password."""
    user = await session.scalar(
        sa.select(User).where(sa.or_(User.email == form_data.username, User.username == form_data.username))
    )
    if not user or not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password.')

    return Token(access_token=create_access_token(email=str(user.email)))


@router.post('/refresh-token', summary='Update access token', status_code=HTTPStatus.OK)
async def refresh_access_token(user: T_CurrentUser) -> Token:
    """Refresh access token."""
    return Token(access_token=create_access_token(email=str(user.email)))


@router.post('/register', summary='Register a new user', status_code=HTTPStatus.CREATED)
async def register(user_data: UserCreate, session: T_DbSession) -> Token:
    """Register a new user and return a JWT token.

    The user details are taken from the request body.
    """
    existing_user = await session.scalar(
        sa.select(User).where(sa.or_(User.email == user_data.username, User.username == user_data.username))
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists',
        )

    new_user = User(email=user_data.email, username=user_data.username, hashed_password=user_data.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return Token(access_token=create_access_token(email=str(new_user.email)))
