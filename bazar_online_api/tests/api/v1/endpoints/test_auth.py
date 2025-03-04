from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from app.core.models import User
from app.main import app

if TYPE_CHECKING:
    from httpx import AsyncClient
else:
    from httpx import AsyncClient  # type: ignore[import]

from app.api.deps import get_current_user


@pytest.mark.asyncio
async def test_register(async_client: AsyncClient) -> None:
    """Test that a new user can register successfully and receive an access token."""
    payload = {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'testpassword',
    }
    response = await async_client.post('/v1/auth/register', json=payload)
    assert response.status_code == HTTPStatus.CREATED, f'Expected {HTTPStatus.CREATED}, got {response.status_code}'
    data = response.json()
    assert 'access_token' in data, 'access_token not found in response'


@pytest.mark.asyncio
async def test_register_existing_user(async_client: AsyncClient) -> None:
    """Test that registering an already existing user returns a 400 error."""
    payload = {
        'email': 'existing@example.com',
        'username': 'existinguser',
        'password': 'somepassword',
    }
    response1 = await async_client.post('/v1/auth/register', json=payload)
    assert response1.status_code == HTTPStatus.CREATED, (
        f'Expected {HTTPStatus.CREATED} on first registration, got {response1.status_code}'
    )
    response2 = await async_client.post('/v1/auth/register', json=payload)
    assert response2.status_code == HTTPStatus.BAD_REQUEST, (
        f'Expected {HTTPStatus.BAD_REQUEST} for duplicate registration, got {response2.status_code}'
    )


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient) -> None:
    """Test that a registered user can log in and receive an access token."""
    reg_payload = {
        'email': 'loginuser@example.com',
        'username': 'loginuser',
        'password': 'loginpassword',
    }
    reg_response = await async_client.post('/v1/auth/register', json=reg_payload)
    assert reg_response.status_code == HTTPStatus.CREATED, (
        f'Registration failed with status {reg_response.status_code}'
    )
    form_data = {
        'username': 'loginuser',
        'password': 'loginpassword',
    }
    login_response = await async_client.post('/v1/auth/login', data=form_data)
    assert login_response.status_code == HTTPStatus.OK, f'Login failed with status {login_response.status_code}'
    data = login_response.json()
    assert 'access_token' in data, 'access_token not found in login response'


@pytest.mark.asyncio
async def test_login_incorrect_credentials(async_client: AsyncClient) -> None:
    """Test that login with incorrect credentials returns a 401 error."""
    payload = {
        'email': 'wronguser@example.com',
        'username': 'wronguser',
        'password': 'correctpassword',
    }
    reg_response = await async_client.post('/v1/auth/register', json=payload)
    assert reg_response.status_code == HTTPStatus.CREATED, (
        f'Registration failed with status {reg_response.status_code}'
    )
    form_data = {
        'username': 'wronguser',
        'password': 'incorrectpassword',
    }
    login_response = await async_client.post('/v1/auth/login', data=form_data)
    assert login_response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Expected {HTTPStatus.UNAUTHORIZED} for incorrect credentials, got {login_response.status_code}'
    )


@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient) -> None:
    """Test that the refresh-token endpoint returns a new access token for an authenticated user."""
    dummy_user = User(
        id=1,
        username='dummyuser',
        email='dummy@example.com',
        hashed_password='dummy_hashed',
    )

    async def override_get_current_user() -> User:
        return dummy_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    refresh_response = await async_client.post('/v1/auth/refresh-token')
    assert refresh_response.status_code == HTTPStatus.OK, (
        f'Expected {HTTPStatus.OK}, got {refresh_response.status_code}'
    )
    data = refresh_response.json()
    assert 'access_token' in data, 'access_token not found in refresh-token response'
    app.dependency_overrides.pop(get_current_user, None)
