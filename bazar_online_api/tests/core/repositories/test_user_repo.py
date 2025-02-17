import pytest
from app.core.repositories.user import UserRepository
from app.core.schemas import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession) -> None:
    """Test for creating a User on the database."""
    repo = UserRepository(session)
    user_in = UserCreate(username='testuser2', email='test23@example.com', password='secret')
    new_user = await repo.create(user_in)
    await session.commit()

    assert new_user.id is not None
    assert new_user.username == 'testuser2'
    assert new_user.email == 'test23@example.com'
    assert new_user.hashed_password != 'secret'


@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession) -> None:
    """Test for fetching a User from the dabatase by the ID."""
    repo = UserRepository(session)
    user_in = UserCreate(username='test2', email='test2@example.com', password='secret2')
    new_user = await repo.create(user_in)
    await session.commit()

    fetched = await repo.get_by_id(int(new_user.id))
    assert fetched is not None
    assert fetched.id == new_user.id


@pytest.mark.asyncio
async def test_get_by_email(session: AsyncSession) -> None:
    """Test for fetching a User from the database by the e-mail."""
    repo = UserRepository(session)
    user_in = UserCreate(username='test3', email='test3@example.com', password='secret3')
    await repo.create(user_in)
    await session.commit()

    fetched = await repo.get_by_email('test3@example.com')
    assert fetched is not None
    assert fetched.email == 'test3@example.com'


@pytest.mark.asyncio
async def test_list_users(session: AsyncSession) -> None:
    """Test for fetching all Users from the dabatase."""
    repo = UserRepository(session)
    initial_users = await repo.list()
    initial_count = len(initial_users)

    user_in = UserCreate(username='listuser', email='listuser@example.com', password='secret')
    await repo.create(user_in)
    await session.commit()

    new_users = await repo.list()
    assert len(new_users) == initial_count + 1


@pytest.mark.asyncio
async def test_update_user(session: AsyncSession) -> None:
    """Test for updating a User on the database."""
    repo = UserRepository(session)
    user_in = UserCreate(username='updateuser', email='update@example.com', password='secret')
    new_user = await repo.create(user_in)
    await session.commit()

    original_hashed = new_user.hashed_password

    update_data = UserUpdate(username='updated', email='updated@example.com', password='newsecret')
    updated_user = await repo.update(new_user, update_data)
    await session.commit()

    assert updated_user.username == 'updated'
    assert updated_user.email == 'updated@example.com'
    assert updated_user.hashed_password != original_hashed


@pytest.mark.asyncio
async def test_delete_user(session: AsyncSession) -> None:
    """Test for deleting a User from the dabatase."""
    repo = UserRepository(session)
    user_in = UserCreate(username='deleteuser', email='delete@example.com', password='secret')
    new_user = await repo.create(user_in)
    await session.commit()

    await repo.delete(new_user)
    await session.commit()

    deleted = await repo.get_by_id(int(new_user.id))
    assert deleted is None
