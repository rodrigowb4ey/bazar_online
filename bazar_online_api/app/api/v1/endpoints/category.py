from http import HTTPStatus

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

from app.api.deps import T_CurrentUser
from app.core.models import Category
from app.core.schemas import CategoryPublic, CategoryPublicList, CategorySchema
from app.infra.database import T_DbSession

router = APIRouter()


@router.get('/', status_code=HTTPStatus.OK)
async def list_categories(session: T_DbSession, current_user: T_CurrentUser) -> list[CategoryPublic]:
    """List all categories owned by the current user."""
    query = sa.select(Category).where(Category.owner_id == current_user.id)
    result = await session.scalars(query)
    categories = list(result.all())
    return CategoryPublicList.validate_python(categories)


@router.get('/{category_id}', status_code=HTTPStatus.OK)
async def get_category(category_id: int, session: T_DbSession, current_user: T_CurrentUser) -> CategoryPublic:
    """Retrieve a specific category by its ID if it belongs to the current user."""
    query = sa.select(Category).where(Category.id == category_id, Category.owner_id == current_user.id)
    category = await session.scalar(query)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    return CategoryPublic.model_validate(category)


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_category(
    category_in: CategorySchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> CategoryPublic:
    """Create a new category with the provided data for the current user."""
    new_category = Category(
        name=category_in.name,
        owner_id=current_user.id,
    )
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return CategoryPublic.model_validate(new_category)


@router.put('/{category_id}', status_code=HTTPStatus.OK)
async def update_category(
    category_id: int,
    category_in: CategorySchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> CategoryPublic:
    """Update an existing category's name for the current user."""
    query = sa.select(Category).where(Category.id == category_id, Category.owner_id == current_user.id)
    category = await session.scalar(query)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    if category_in.name is not None:
        category.name = category_in.name
    await session.commit()
    await session.refresh(category)
    return CategoryPublic.model_validate(category)


@router.delete('/{category_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_category(
    category_id: int,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> None:
    """Delete a category by its ID if it belongs to the current user."""
    query = sa.select(Category).where(Category.id == category_id, Category.owner_id == current_user.id)
    category = await session.scalar(query)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    await session.delete(category)
    await session.commit()
