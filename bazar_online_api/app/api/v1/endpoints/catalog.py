from http import HTTPStatus

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

from app.api.deps import T_CurrentUser
from app.core.models import Catalog
from app.core.schemas import CatalogPublic, CatalogPublicList, CatalogSchema
from app.infra.database import T_DbSession

router = APIRouter()


@router.get('/', status_code=HTTPStatus.OK)
async def list_catalogs(session: T_DbSession, current_user: T_CurrentUser) -> list[CatalogPublic]:
    """List all catalogs owned by the current user."""
    query = sa.select(Catalog).where(Catalog.owner_id == current_user.id)
    result = await session.scalars(query)
    catalogs = list(result.all())
    return CatalogPublicList.validate_python(catalogs)


@router.get('/{catalog_id}', status_code=HTTPStatus.OK)
async def get_catalog(catalog_id: int, session: T_DbSession, current_user: T_CurrentUser) -> CatalogPublic:
    """Retrieve a specific catalog by its ID if it belongs to the current user."""
    query = sa.select(Catalog).where(Catalog.id == catalog_id, Catalog.owner_id == current_user.id)
    catalog = await session.scalar(query)
    if not catalog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Catalog not found')
    return CatalogPublic.model_validate(catalog)


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_catalog(
    catalog_in: CatalogSchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> CatalogPublic:
    """Create a new catalog with the provided data for the current user."""
    new_catalog = Catalog(
        name=catalog_in.name,
        description=catalog_in.description,
        owner_id=current_user.id,
    )
    session.add(new_catalog)
    await session.commit()
    await session.refresh(new_catalog)
    return CatalogPublic.model_validate(new_catalog)


@router.put('/{catalog_id}', status_code=HTTPStatus.OK)
async def update_catalog(
    catalog_id: int,
    catalog_in: CatalogSchema,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> CatalogPublic:
    """Update an existing catalog for the current user."""
    query = sa.select(Catalog).where(Catalog.id == catalog_id, Catalog.owner_id == current_user.id)
    catalog = await session.scalar(query)
    if not catalog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Catalog not found')
    if catalog_in.name is not None:
        catalog.name = catalog_in.name
    if catalog_in.description is not None:
        catalog.description = catalog_in.description
    await session.commit()
    await session.refresh(catalog)
    return CatalogPublic.model_validate(catalog)


@router.delete('/{catalog_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_catalog(
    catalog_id: int,
    session: T_DbSession,
    current_user: T_CurrentUser,
) -> None:
    """Delete a catalog by its ID if it belongs to the current user."""
    query = sa.select(Catalog).where(Catalog.id == catalog_id, Catalog.owner_id == current_user.id)
    catalog = await session.scalar(query)
    if not catalog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Catalog not found')
    await session.delete(catalog)
    await session.commit()
