from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Category
from app.core.schemas import CategoryCreate, CategoryUpdate


class CategoryRepository:
    """Repository for Category CRUD actions."""

    def __init__(self, session: AsyncSession) -> None:
        """Constructor."""
        self.session = session

    async def create(self, category_in: CategoryCreate) -> Category:
        """Create a new Category.

        Args:
            category_in: Pydantic schema containing the data for the new category.

        Returns:
            The created Category model instance.
        """
        new_category = Category(
            name=category_in.name,
            owner_id=category_in.owner_id,
        )
        self.session.add(new_category)
        await self.session.flush()  # flush to assign an ID
        return new_category

    async def get_by_id(self, category_id: int) -> Category | None:
        """Retrieve a Category by its ID.

        Args:
            category_id: The ID of the category to retrieve.

        Returns:
            The Category instance if found, else None.
        """
        result = await self.session.execute(select(Category).filter(Category.id == category_id))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """List Categories with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of Category instances.
        """
        result = await self.session.execute(select(Category).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, category: Category, category_in: CategoryUpdate) -> Category:
        """Update an existing Category.

        Args:
            category: The existing Category instance.
            category_in: Pydantic schema with updated data.

        Returns:
            The updated Category instance.
        """
        update_data = category_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        self.session.add(category)
        await self.session.flush()
        return category

    async def delete(self, category: Category) -> None:
        """Delete a Category.

        Args:
            category: The Category instance to delete.
        """
        await self.session.delete(category)
        await self.session.flush()
