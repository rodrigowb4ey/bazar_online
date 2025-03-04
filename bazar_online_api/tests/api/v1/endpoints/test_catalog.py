from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_catalog(async_client: AsyncClient, token: str) -> None:
    """Test that a new catalog can be created."""
    payload = {'name': 'TestCatalog', 'description': 'A sample catalog'}
    response = await async_client.post('/v1/catalogs/', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.CREATED, f'Expected {HTTPStatus.CREATED}, got {response.status_code}'
    data = response.json()
    assert data['name'] == 'TestCatalog'
    assert data['description'] == 'A sample catalog'


@pytest.mark.asyncio
async def test_list_catalogs(async_client: AsyncClient, token: str) -> None:
    """Test that listing catalogs returns the expected number."""
    payload1 = {'name': 'CatalogOne', 'description': 'First catalog'}
    payload2 = {'name': 'CatalogTwo', 'description': 'Second catalog'}
    await async_client.post('/v1/catalogs/', json=payload1, headers={'Authorization': f'Bearer {token}'})
    await async_client.post('/v1/catalogs/', json=payload2, headers={'Authorization': f'Bearer {token}'})
    response = await async_client.get('/v1/catalogs/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert isinstance(data, list)
    expected_catalog_count = 2
    assert len(data) == expected_catalog_count, f'Expected {expected_catalog_count} catalogs, got {len(data)}'


@pytest.mark.asyncio
async def test_get_catalog(async_client: AsyncClient, token: str) -> None:
    """Test that a catalog can be retrieved by ID."""
    payload = {'name': 'SingleCatalog', 'description': 'Only catalog'}
    create_resp = await async_client.post('/v1/catalogs/', json=payload, headers={'Authorization': f'Bearer {token}'})
    catalog_id = create_resp.json()['id']
    response = await async_client.get(f'/v1/catalogs/{catalog_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert data['id'] == catalog_id
    assert data['name'] == 'SingleCatalog'
    assert data['description'] == 'Only catalog'


@pytest.mark.asyncio
async def test_get_catalog_not_found(async_client: AsyncClient, token: str) -> None:
    """Test that a non-existent catalog returns 404."""
    response = await async_client.get('/v1/catalogs/999999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {response.status_code}'


@pytest.mark.asyncio
async def test_update_catalog(async_client: AsyncClient, token: str) -> None:
    """Test that a catalog can be updated."""
    payload = {'name': 'OldCatalog', 'description': 'Old description'}
    create_resp = await async_client.post('/v1/catalogs/', json=payload, headers={'Authorization': f'Bearer {token}'})
    catalog_id = create_resp.json()['id']
    update_payload = {'name': 'NewCatalog', 'description': 'New description'}
    update_resp = await async_client.put(
        f'/v1/catalogs/{catalog_id}', json=update_payload, headers={'Authorization': f'Bearer {token}'}
    )
    assert update_resp.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {update_resp.status_code}'
    data = update_resp.json()
    assert data['name'] == 'NewCatalog'
    assert data['description'] == 'New description'


@pytest.mark.asyncio
async def test_delete_catalog(async_client: AsyncClient, token: str) -> None:
    """Test that a catalog can be deleted."""
    payload = {'name': 'DeleteCatalog', 'description': 'To be deleted'}
    create_resp = await async_client.post('/v1/catalogs/', json=payload, headers={'Authorization': f'Bearer {token}'})
    catalog_id = create_resp.json()['id']
    delete_resp = await async_client.delete(f'/v1/catalogs/{catalog_id}', headers={'Authorization': f'Bearer {token}'})
    assert delete_resp.status_code == HTTPStatus.NO_CONTENT, (
        f'Expected {HTTPStatus.NO_CONTENT}, got {delete_resp.status_code}'
    )
    get_resp = await async_client.get(f'/v1/catalogs/{catalog_id}', headers={'Authorization': f'Bearer {token}'})
    assert get_resp.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {get_resp.status_code}'
