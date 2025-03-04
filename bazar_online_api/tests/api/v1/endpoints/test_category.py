from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(async_client: AsyncClient, token: str) -> None:
    """Test that a new category can be created for the current user."""
    payload = {'name': 'Test Category'}
    response = await async_client.post('/v1/categories/', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.CREATED, f'Expected {HTTPStatus.CREATED}, got {response.status_code}'
    data = response.json()
    assert data['name'] == 'Test Category'


@pytest.mark.asyncio
async def test_list_categories(async_client: AsyncClient, token: str) -> None:
    """Test that listing categories returns only those owned by the current user."""
    payload1 = {'name': 'Cat One'}
    payload2 = {'name': 'Cat Two'}
    await async_client.post('/v1/categories/', json=payload1, headers={'Authorization': f'Bearer {token}'})
    await async_client.post('/v1/categories/', json=payload2, headers={'Authorization': f'Bearer {token}'})
    response = await async_client.get('/v1/categories/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert isinstance(data, list)
    num_of_categories = 2
    assert len(data) == num_of_categories, f'Expected {num_of_categories} categories, got {len(data)}'


@pytest.mark.asyncio
async def test_get_category(async_client: AsyncClient, token: str) -> None:
    """Test that a category can be retrieved by its ID."""
    payload = {'name': 'Single Category'}
    create_resp = await async_client.post(
        '/v1/categories/', json=payload, headers={'Authorization': f'Bearer {token}'}
    )
    cat_id = create_resp.json()['id']
    response = await async_client.get(f'/v1/categories/{cat_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert data['id'] == cat_id
    assert data['name'] == 'Single Category'


@pytest.mark.asyncio
async def test_get_category_not_found(async_client: AsyncClient, token: str) -> None:
    """Test that retrieving a non-existent category returns a 404."""
    response = await async_client.get('/v1/categories/999999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {response.status_code}'


@pytest.mark.asyncio
async def test_update_category(async_client: AsyncClient, token: str) -> None:
    """Test that a category's name can be updated."""
    payload = {'name': 'Old Name'}
    create_resp = await async_client.post(
        '/v1/categories/', json=payload, headers={'Authorization': f'Bearer {token}'}
    )
    cat_id = create_resp.json()['id']
    update_payload = {'name': 'New Name'}
    update_resp = await async_client.put(
        f'/v1/categories/{cat_id}', json=update_payload, headers={'Authorization': f'Bearer {token}'}
    )
    assert update_resp.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {update_resp.status_code}'
    data = update_resp.json()
    assert data['name'] == 'New Name'


@pytest.mark.asyncio
async def test_delete_category(async_client: AsyncClient, token: str) -> None:
    """Test that a category can be deleted and is no longer retrievable."""
    payload = {'name': 'Delete Me'}
    create_resp = await async_client.post(
        '/v1/categories/', json=payload, headers={'Authorization': f'Bearer {token}'}
    )
    cat_id = create_resp.json()['id']
    delete_resp = await async_client.delete(f'/v1/categories/{cat_id}', headers={'Authorization': f'Bearer {token}'})
    assert delete_resp.status_code == HTTPStatus.NO_CONTENT, (
        f'Expected {HTTPStatus.NO_CONTENT}, got {delete_resp.status_code}'
    )
    get_resp = await async_client.get(f'/v1/categories/{cat_id}', headers={'Authorization': f'Bearer {token}'})
    assert get_resp.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {get_resp.status_code}'
