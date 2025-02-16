from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating User instances."""

    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating User instances."""

    username: str | None = None
    email: str | None = None
    password: str | None = None
