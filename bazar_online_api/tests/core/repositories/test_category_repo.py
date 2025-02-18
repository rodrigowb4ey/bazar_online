import pytest
from app.core.repositories.category import CategoryRepository
from app.core.schemas import CategoryCreate, CategoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_category(session: AsyncSession) -> None:
    """Test creating a Category in the database."""
    repo = CategoryRepository(session)
    category_in = CategoryCreate(name='Electronics', owner_id=1)
    new_category = await repo.create(category_in)
    await session.commit()

    assert new_category.id is not None
    assert new_category.name == 'Electronics'
    assert new_category.owner_id == 1


@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession) -> None:
    """Test fetching a Category by its ID."""
    repo = CategoryRepository(session)
    category_in = CategoryCreate(name='Books', owner_id=2)
    new_category = await repo.create(category_in)
    await session.commit()

    fetched = await repo.get_by_id(int(new_category.id))
    assert fetched is not None
    assert fetched.id == new_category.id
    assert fetched.name == 'Books'


@pytest.mark.asyncio
async def test_list_categories_by_owner_id(session: AsyncSession) -> None:
    """Test listing Categories by Owner ID."""
    repo = CategoryRepository(session)
    initial_categories = await repo.list_by_owner_id(owner_id=3)
    initial_count = len(initial_categories)

    category_in = CategoryCreate(name='Toys', owner_id=3)
    await repo.create(category_in)
    await session.commit()

    new_categories = await repo.list_by_owner_id(owner_id=3)
    assert len(new_categories) == initial_count + 1


@pytest.mark.asyncio
async def test_update_category(session: AsyncSession) -> None:
    """Test updating an existing Category."""
    repo = CategoryRepository(session)
    category_in = CategoryCreate(name='Clothes', owner_id=4)
    new_category = await repo.create(category_in)
    await session.commit()

    original_name = new_category.name

    update_data = CategoryUpdate(name='Apparel')
    updated_category = await repo.update(new_category, update_data)
    await session.commit()

    assert updated_category.name == 'Apparel'
    assert updated_category.name != original_name


@pytest.mark.asyncio
async def test_delete_category(session: AsyncSession) -> None:
    """Test deleting a Category."""
    repo = CategoryRepository(session)
    category_in = CategoryCreate(name='Furniture', owner_id=5)
    new_category = await repo.create(category_in)
    await session.commit()

    await repo.delete(new_category)
    await session.commit()

    deleted = await repo.get_by_id(int(new_category.id))
    assert deleted is None
