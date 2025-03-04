"""Refactor models to SQLAlchemy 2.0 typed API.

Revision ID: f60a24a2dca7
Revises: 22bea670ab89
Create Date: 2025-03-04 13:41:19.352933

"""

from collections.abc import Sequence

from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f60a24a2dca7'
down_revision: str | None = '22bea670ab89'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration to the database."""
    op.alter_column('catalogs', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('catalogs', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('categories', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('categories', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('products', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('products', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('users', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('users', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)


def downgrade() -> None:
    """Rollback the migration."""
    op.alter_column('users', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('users', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('products', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('products', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('categories', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('categories', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('catalogs', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('catalogs', 'created_at', existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
