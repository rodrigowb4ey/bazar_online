from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import User
from app.core.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRepository:
    """Repository for User CRUD actions."""

    def __init__(self, session: AsyncSession) -> None:
        """Constructor."""
        self.session = session

    async def create(self, user_in: UserCreate) -> User:
        """Create an User."""
        hashed_password = pwd_context.hash(user_in.password)
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def get_by_id(self, user_id: int) -> User | None:
        """Get User by id."""
        result = await self.session.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get User by e-mail."""
        result = await self.session.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List Users within a specific range."""
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, user: User, user_in: UserUpdate) -> User:
        """Update User."""
        update_data = user_in.model_dump(exclude_unset=True)
        if update_data.get('password'):
            update_data['hashed_password'] = pwd_context.hash(update_data.pop('password'))
        for field, value in update_data.items():
            setattr(user, field, value)
        self.session.add(user)
        await self.session.flush()
        return user

    async def delete(self, user: User) -> None:
        """Delete User."""
        await self.session.delete(user)
        await self.session.flush()
