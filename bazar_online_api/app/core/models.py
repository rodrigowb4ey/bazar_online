from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy's Base class."""


class User(Base):
    """Users table."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    catalogs: Mapped[list['Catalog']] = relationship('Catalog', back_populates='owner', cascade='all, delete-orphan')
    products: Mapped[list['Product']] = relationship('Product', back_populates='owner', cascade='all, delete-orphan')
    categories: Mapped[list['Category']] = relationship(
        'Category', back_populates='owner', cascade='all, delete-orphan'
    )


class Catalog(Base):
    """Catalogs table."""

    __tablename__ = 'catalogs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    owner: Mapped['User'] = relationship('User', back_populates='catalogs')
    products: Mapped[list['Product']] = relationship('Product', back_populates='catalog', cascade='all, delete-orphan')


class Category(Base):
    """Categories table."""

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    owner: Mapped['User'] = relationship('User', back_populates='categories')
    products: Mapped[list['Product']] = relationship(
        'Product', back_populates='category', cascade='all, delete-orphan'
    )


class Product(Base):
    """Products table."""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    catalog_id: Mapped[int] = mapped_column(Integer, ForeignKey('catalogs.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    catalog: Mapped['Catalog'] = relationship('Catalog', back_populates='products')
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    owner: Mapped['User'] = relationship('User', back_populates='products')
