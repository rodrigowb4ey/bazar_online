import pytest
from app.core.repositories.product import ProductRepository
from app.core.schemas import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_product(session: AsyncSession) -> None:
    """Test for creating a Product in the database."""
    price = 1500.0
    repo = ProductRepository(session)
    product_in = ProductCreate(
        name='Laptop',
        description='A powerful laptop',
        price=1500.0,
        catalog_id=1,
        category_id=2,
        owner_id=3,
    )
    new_product = await repo.create(product_in)
    await session.commit()

    assert new_product.id is not None
    assert new_product.name == 'Laptop'
    assert new_product.price == price
    assert new_product.description == 'A powerful laptop'


@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession) -> None:
    """Test for fetching a Product by its ID."""
    repo = ProductRepository(session)
    product_in = ProductCreate(
        name='Phone',
        description='A smartphone',
        price=800.0,
        catalog_id=1,
        category_id=2,
        owner_id=3,
    )
    new_product = await repo.create(product_in)
    await session.commit()

    fetched = await repo.get_by_id(int(new_product.id))
    assert fetched is not None
    assert fetched.id == new_product.id
    assert fetched.name == 'Phone'


@pytest.mark.asyncio
async def test_list_products(session: AsyncSession) -> None:
    """Test for listing Products with pagination."""
    repo = ProductRepository(session)
    initial_products = await repo.list()
    initial_count = len(initial_products)

    product_in = ProductCreate(
        name='Tablet',
        description='A portable tablet',
        price=500.0,
        catalog_id=1,
        category_id=2,
        owner_id=3,
    )
    await repo.create(product_in)
    await session.commit()

    new_products = await repo.list()
    assert len(new_products) == initial_count + 1


@pytest.mark.asyncio
async def test_update_product(session: AsyncSession) -> None:
    """Test for updating an existing Product."""
    repo = ProductRepository(session)
    product_in = ProductCreate(
        name='Monitor',
        description='24-inch monitor',
        price=300.0,
        catalog_id=1,
        category_id=2,
        owner_id=3,
    )
    new_product = await repo.create(product_in)
    await session.commit()

    original_price = new_product.price

    update_data = ProductUpdate(name='Monitor Pro', description='27-inch monitor', price=350.0)
    updated_product = await repo.update(new_product, update_data)
    await session.commit()

    assert updated_product.name == 'Monitor Pro'
    assert updated_product.description == '27-inch monitor'
    assert updated_product.price != original_price


@pytest.mark.asyncio
async def test_delete_product(session: AsyncSession) -> None:
    """Test for deleting a Product from the database."""
    repo = ProductRepository(session)
    product_in = ProductCreate(
        name='Keyboard',
        description='Mechanical keyboard',
        price=120.0,
        catalog_id=1,
        category_id=2,
        owner_id=3,
    )
    new_product = await repo.create(product_in)
    await session.commit()

    await repo.delete(new_product)
    await session.commit()

    deleted = await repo.get_by_id(int(new_product.id))
    assert deleted is None
