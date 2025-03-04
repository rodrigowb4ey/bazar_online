from http import HTTPStatus

import pytest
from app.core.models import Catalog, Category
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient, token: str, catalog: Catalog, category: Category) -> None:
    """Test that a new product can be created."""
    payload = {
        'name': 'TestProduct',
        'description': 'A sample product',
        'price': 9.99,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    expected_price = 9.99
    response = await async_client.post('/v1/products/', json=payload, headers={'Authorization': f'Bearer {token}'})
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED, f'Expected {HTTPStatus.CREATED}, got {response.status_code}'
    assert data['name'] == 'TestProduct'
    assert data['description'] == 'A sample product'
    assert float(data['price']) == expected_price
    assert data['catalog_id'] == catalog.id
    assert data['category_id'] == category.id
    assert data['owner_id'] == 1


@pytest.mark.asyncio
async def test_list_products(async_client: AsyncClient, token: str, catalog: Catalog, category: Category) -> None:
    """Test that listing products returns the expected number."""
    payload1 = {
        'name': 'ProductOne',
        'description': 'First product',
        'price': 1.99,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    payload2 = {
        'name': 'ProductTwo',
        'description': 'Second product',
        'price': 2.99,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    await async_client.post('/v1/products/', json=payload1, headers={'Authorization': f'Bearer {token}'})
    await async_client.post('/v1/products/', json=payload2, headers={'Authorization': f'Bearer {token}'})
    response = await async_client.get('/v1/products/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert isinstance(data, list)
    expected_count = 2
    assert len(data) == expected_count, f'Expected {expected_count} products, got {len(data)}'
    for item in data:
        assert item['owner_id'] == 1


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient, token: str, catalog: Catalog, category: Category) -> None:
    """Test that a product can be retrieved by its ID."""
    payload = {
        'name': 'SingleProduct',
        'description': 'Only product',
        'price': 5.55,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    expected_price = 5.55
    create_resp = await async_client.post('/v1/products/', json=payload, headers={'Authorization': f'Bearer {token}'})
    prod_id = create_resp.json()['id']
    response = await async_client.get(f'/v1/products/{prod_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {response.status_code}'
    data = response.json()
    assert data['id'] == prod_id
    assert data['name'] == 'SingleProduct'
    assert data['description'] == 'Only product'
    assert float(data['price']) == expected_price


@pytest.mark.asyncio
async def test_get_product_not_found(async_client: AsyncClient, token: str) -> None:
    """Test that a non-existent product returns a 404."""
    response = await async_client.get('/v1/products/999999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {response.status_code}'


@pytest.mark.asyncio
async def test_update_product(async_client: AsyncClient, token: str, catalog: Catalog, category: Category) -> None:
    """Test that a product can be updated."""
    payload = {
        'name': 'OldProduct',
        'description': 'Old description',
        'price': 3.33,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    expected_price = 4.44
    create_resp = await async_client.post('/v1/products/', json=payload, headers={'Authorization': f'Bearer {token}'})
    prod_id = create_resp.json()['id']
    update_payload = {
        'name': 'NewProduct',
        'description': 'New description',
        'price': 4.44,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    update_resp = await async_client.put(
        f'/v1/products/{prod_id}', json=update_payload, headers={'Authorization': f'Bearer {token}'}
    )
    assert update_resp.status_code == HTTPStatus.OK, f'Expected {HTTPStatus.OK}, got {update_resp.status_code}'
    data = update_resp.json()
    assert data['name'] == 'NewProduct'
    assert data['description'] == 'New description'
    assert float(data['price']) == expected_price


@pytest.mark.asyncio
async def test_delete_product(async_client: AsyncClient, token: str, catalog: Catalog, category: Category) -> None:
    """Test that a product can be deleted."""
    payload = {
        'name': 'DeleteProduct',
        'description': 'To be deleted',
        'price': 2.22,
        'catalog_id': catalog.id,
        'category_id': category.id,
    }
    create_resp = await async_client.post('/v1/products/', json=payload, headers={'Authorization': f'Bearer {token}'})
    prod_id = create_resp.json()['id']
    delete_resp = await async_client.delete(f'/v1/products/{prod_id}', headers={'Authorization': f'Bearer {token}'})
    assert delete_resp.status_code == HTTPStatus.NO_CONTENT, (
        f'Expected {HTTPStatus.NO_CONTENT}, got {delete_resp.status_code}'
    )
    get_resp = await async_client.get(f'/v1/products/{prod_id}', headers={'Authorization': f'Bearer {token}'})
    assert get_resp.status_code == HTTPStatus.NOT_FOUND, f'Expected {HTTPStatus.NOT_FOUND}, got {get_resp.status_code}'
