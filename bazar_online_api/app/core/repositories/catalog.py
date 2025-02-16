from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Catalog
from app.core.schemas import CatalogCreate, CatalogUpdate


class CatalogRepository:
    """Repository for Catalog CRUD actions."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async SQLAlchemy session."""
        self.session = session

    async def create(self, catalog_in: CatalogCreate) -> Catalog:
        """Create a new Catalog.

        Args:
            catalog_in: Pydantic schema containing the data for the new catalog.

        Returns:
            The created Catalog instance.
        """
        new_catalog = Catalog(
            name=catalog_in.name,
            description=catalog_in.description,
            owner_id=catalog_in.owner_id,
        )
        self.session.add(new_catalog)
        await self.session.flush()  # flush to assign an ID
        return new_catalog

    async def get_by_id(self, catalog_id: int) -> Catalog | None:
        """Retrieve a Catalog by its ID.

        Args:
            catalog_id: The ID of the catalog to retrieve.

        Returns:
            The Catalog instance if found, else None.
        """
        result = await self.session.execute(select(Catalog).filter(Catalog.id == catalog_id))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Catalog]:
        """List Catalogs with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of Catalog instances.
        """
        result = await self.session.execute(select(Catalog).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, catalog: Catalog, catalog_in: CatalogUpdate) -> Catalog:
        """Update an existing Catalog.

        Args:
            catalog: The existing Catalog instance.
            catalog_in: Pydantic schema with updated data.

        Returns:
            The updated Catalog instance.
        """
        update_data = catalog_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(catalog, field, value)
        self.session.add(catalog)
        await self.session.flush()
        return catalog

    async def delete(self, catalog: Catalog) -> None:
        """Delete a Catalog.

        Args:
            catalog: The Catalog instance to delete.
        """
        await self.session.delete(catalog)
        await self.session.flush()
