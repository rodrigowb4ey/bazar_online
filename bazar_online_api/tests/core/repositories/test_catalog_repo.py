import pytest
from app.core.repositories.catalog import CatalogRepository
from app.core.schemas import CatalogCreate, CatalogUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_catalog(session: AsyncSession) -> None:
    """Test for creating a Catalog in the database."""
    repo = CatalogRepository(session)
    catalog_in = CatalogCreate(name='Summer Sale', description='Discounts on summer items', owner_id=1)
    new_catalog = await repo.create(catalog_in)
    await session.commit()

    assert new_catalog.id is not None
    assert new_catalog.name == 'Summer Sale'
    assert new_catalog.description == 'Discounts on summer items'
    assert new_catalog.owner_id == 1


@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession) -> None:
    """Test for fetching a Catalog by its ID."""
    repo = CatalogRepository(session)
    catalog_in = CatalogCreate(name='Winter Collection', description='New winter arrivals', owner_id=2)
    new_catalog = await repo.create(catalog_in)
    await session.commit()

    fetched = await repo.get_by_id(int(new_catalog.id))
    assert fetched is not None
    assert fetched.id == new_catalog.id
    assert fetched.name == 'Winter Collection'


@pytest.mark.asyncio
async def test_list_catalogs(session: AsyncSession) -> None:
    """Test for listing Catalogs with pagination."""
    repo = CatalogRepository(session)
    initial_catalogs = await repo.list()
    initial_count = len(initial_catalogs)

    catalog_in = CatalogCreate(name='Accessories', description='Fashion accessories', owner_id=3)
    await repo.create(catalog_in)
    await session.commit()

    new_catalogs = await repo.list()
    assert len(new_catalogs) == initial_count + 1


@pytest.mark.asyncio
async def test_update_catalog(session: AsyncSession) -> None:
    """Test for updating an existing Catalog."""
    repo = CatalogRepository(session)
    catalog_in = CatalogCreate(name='Old Catalog', description='Old description', owner_id=4)
    new_catalog = await repo.create(catalog_in)
    await session.commit()

    original_name = new_catalog.name

    update_data = CatalogUpdate(name='Updated Catalog', description='Updated description')
    updated_catalog = await repo.update(new_catalog, update_data)
    await session.commit()

    assert updated_catalog.name == 'Updated Catalog'
    assert updated_catalog.description == 'Updated description'
    assert updated_catalog.name != original_name


@pytest.mark.asyncio
async def test_delete_catalog(session: AsyncSession) -> None:
    """Test for deleting a Catalog from the database."""
    repo = CatalogRepository(session)
    catalog_in = CatalogCreate(name='To Delete', description='Catalog to be deleted', owner_id=5)
    new_catalog = await repo.create(catalog_in)
    await session.commit()

    await repo.delete(new_catalog)
    await session.commit()

    deleted = await repo.get_by_id(int(new_catalog.id))
    assert deleted is None
