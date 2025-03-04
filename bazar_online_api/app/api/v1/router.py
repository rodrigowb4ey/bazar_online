from fastapi import APIRouter

from app.api.v1.endpoints import auth, catalog, category

router = APIRouter()

router.include_router(auth.router, prefix='/auth', tags=['auth'])
router.include_router(category.router, prefix='/categories', tags=['categories'])
router.include_router(catalog.router, prefix='/catalogs', tags=['catalogs'])
