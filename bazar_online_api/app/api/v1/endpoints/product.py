from http import HTTPStatus

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

from app.api.deps import T_CurrentUser
from app.core.models import Product
from app.core.schemas import ProductPublic, ProductPublicList, ProductSchema
from app.infra.database import T_DbSession

router = APIRouter()


@router.get('/', status_code=HTTPStatus.OK)
async def list_products(session: T_DbSession, current_user: T_CurrentUser) -> list[ProductPublic]:
    """List all products owned by the current user."""
    query = sa.select(Product).where(Product.owner_id == current_user.id)
    result = await session.scalars(query)
    products = list(result.all())
    return ProductPublicList.validate_python(products)


@router.get('/{product_id}', status_code=HTTPStatus.OK)
async def get_product(product_id: int, session: T_DbSession, current_user: T_CurrentUser) -> ProductPublic:
    """Retrieve a product by ID if it belongs to the current user."""
    query = sa.select(Product).where(Product.id == product_id, Product.owner_id == current_user.id)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return ProductPublic.model_validate(product)


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_product(
    product_in: ProductSchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> ProductPublic:
    """Create a new product with the provided data for the current user."""
    new_product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        catalog_id=product_in.catalog_id,
        category_id=product_in.category_id,
        owner_id=current_user.id,
    )
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return ProductPublic.model_validate(new_product)


@router.put('/{product_id}', status_code=HTTPStatus.OK)
async def update_product(
    product_id: int,
    product_in: ProductSchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> ProductPublic:
    """Update an existing product for the current user."""
    query = sa.select(Product).where(Product.id == product_id, Product.owner_id == current_user.id)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    if product_in.name is not None:
        product.name = product_in.name
    product.description = product_in.description
    product.price = product_in.price
    product.catalog_id = product_in.catalog_id
    product.category_id = product_in.category_id
    await session.commit()
    await session.refresh(product)
    return ProductPublic.model_validate(product)


@router.delete('/{product_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_product(
    product_id: int,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> None:
    """Delete a product by its ID if it belongs to the current user."""
    query = sa.select(Product).where(Product.id == product_id, Product.owner_id == current_user.id)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    await session.delete(product)
    await session.commit()
