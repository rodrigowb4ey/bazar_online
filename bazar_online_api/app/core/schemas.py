from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.core.security import get_password_hash


class UserCreate(BaseModel):
    """Schema for creating User instances."""

    email: str
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

    @field_validator('username')
    @classmethod
    def username_validate(cls, v: str) -> str:
        """Validation for 'username' field."""
        if ' ' in v:
            raise ValueError('username field cannot have blank spaces.')
        return v

    @field_validator('password')
    @classmethod
    def password_validate(cls, v: str) -> str:
        """Validation for 'password' field."""
        return get_password_hash(v)


class UserUpdate(BaseModel):
    """Schema for updating User instances."""

    username: str | None = None
    email: str | None = None
    password: str | None = None


class CategoryCreate(BaseModel):
    """Schema for creating Category instances."""

    name: str
    owner_id: int


class CategoryUpdate(BaseModel):
    """Schema for updating Category instances."""

    name: str | None = None


class ProductCreate(BaseModel):
    """Schema for creating a Product."""

    name: str
    description: str | None = None
    price: float
    catalog_id: int
    category_id: int
    owner_id: int


class ProductUpdate(BaseModel):
    """Schema for updating a Product."""

    name: str | None = None
    description: str | None = None
    price: float | None = None
    catalog_id: int | None = None
    category_id: int | None = None
    owner_id: int | None = None


class CatalogCreate(BaseModel):
    """Schema for creating a Catalog."""

    name: str
    description: str | None = None
    owner_id: int


class CatalogUpdate(BaseModel):
    """Schema for updating a Catalog."""

    name: str | None = None
    description: str | None = None


class Token(BaseModel):
    """Schema for access token."""

    token_type: Literal['bearer'] = 'bearer'  # noqa: S105
    access_token: str
