from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Product
from app.core.schemas import ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for Product CRUD actions."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async SQLAlchemy session."""
        self.session = session

    async def create(self, product_in: ProductCreate) -> Product:
        """Create a new Product.

        Args:
            product_in: Pydantic schema containing the data for the new product.

        Returns:
            The created Product instance.
        """
        new_product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            catalog_id=product_in.catalog_id,
            category_id=product_in.category_id,
            owner_id=product_in.owner_id,
        )
        self.session.add(new_product)
        await self.session.flush()  # Flush to assign an ID and synchronize state.
        return new_product

    async def get_by_id(self, product_id: int) -> Product | None:
        """Retrieve a Product by its ID.

        Args:
            product_id: The ID of the product to retrieve.

        Returns:
            The Product instance if found, else None.
        """
        result = await self.session.execute(select(Product).filter(Product.id == product_id))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """List Products with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of Product instances.
        """
        result = await self.session.execute(select(Product).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, product: Product, product_in: ProductUpdate) -> Product:
        """Update an existing Product.

        Args:
            product: The existing Product instance.
            product_in: Pydantic schema with updated product data.

        Returns:
            The updated Product instance.
        """
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        self.session.add(product)
        await self.session.flush()
        return product

    async def delete(self, product: Product) -> None:
        """Delete a Product.

        Args:
            product: The Product instance to delete.
        """
        await self.session.delete(product)
        await self.session.flush()
