from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """SQLAlchemy's Base class."""


class User(Base):
    """Users table."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    catalogs = relationship('Catalog', back_populates='owner', cascade='all, delete-orphan')
    products = relationship('Product', back_populates='owner', cascade='all, delete-orphan')
    categories = relationship('Category', back_populates='owner', cascade='all, delete-orphan')


class Catalog(Base):
    """Catalogs table."""

    __tablename__ = 'catalogs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    owner = relationship('User', back_populates='catalogs')
    products = relationship('Product', back_populates='catalog', cascade='all, delete-orphan')


class Category(Base):
    """Categories table."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    owner = relationship('User', back_populates='categories')
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')


class Product(Base):
    """Products table."""

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalogs.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    catalog = relationship('Catalog', back_populates='products')
    category = relationship('Category', back_populates='products')
    owner = relationship('User', back_populates='products')
