from http import HTTPStatus

import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_register_and_login() -> None:
    """Test that registers a user and then logs in with the same credentials."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        register_payload: dict[str, str] = {'username': 'testuser', 'email': 'test@example.com', 'password': 'secret'}
        reg_response = await ac.post('/v1/auth/register', json=register_payload)
        assert reg_response.status_code == HTTPStatus.OK, f'Registration failed: {reg_response.text}'
        reg_json = reg_response.json()
        assert 'access_token' in reg_json, 'No access_token in registration response'

        login_payload: dict[str, str] = {
            'username': 'test@example.com',
            'password': 'secret',
        }
        login_response = await ac.post('/v1/auth/login', data=login_payload)
        assert login_response.status_code == HTTPStatus.OK, f'Login failed: {login_response.text}'
        login_json = login_response.json()
        assert 'access_token' in login_json, 'No access_token in login response'


@pytest.mark.asyncio
async def test_login_invalid_credentials() -> None:
    """Test login with an incorrect password for an existing user."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        register_payload: dict[str, str] = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'correctpassword',
        }
        reg_response = await ac.post('/v1/auth/register', json=register_payload)
        assert reg_response.status_code == HTTPStatus.OK

        login_payload: dict[str, str] = {'username': 'other@example.com', 'password': 'wrongpassword'}
        login_response = await ac.post('/v1/auth/login', data=login_payload)
        assert login_response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_nonexistent_user() -> None:
    """Test login for a user that doesn't exist."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        login_payload: dict[str, str] = {'username': 'nonexistent@example.com', 'password': 'any'}
        login_response = await ac.post('/v1/auth/login', data=login_payload)
        assert login_response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_register_duplicate_user() -> None:
    """Test duplicate registration returns an error."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        register_payload: dict[str, str] = {'username': 'dupuser', 'email': 'dup@example.com', 'password': 'secret'}
        reg_response1 = await ac.post('/v1/auth/register', json=register_payload)
        assert reg_response1.status_code == HTTPStatus.OK, f'First registration failed: {reg_response1.text}'
        reg_response2 = await ac.post('/v1/auth/register', json=register_payload)
        assert reg_response2.status_code == HTTPStatus.BAD_REQUEST, (
            f'Duplicate registration did not fail as expected: {reg_response2.text}'
        )
