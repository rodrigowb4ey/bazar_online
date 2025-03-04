"""Changing price from float to decimal.

Revision ID: f19093c62313
Revises: f60a24a2dca7
Create Date: 2025-03-04 16:07:09.634184

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f19093c62313'
down_revision: str | None = 'f60a24a2dca7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration to the database."""
    op.alter_column(
        'products',
        'price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric(precision=10, scale=2),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Rollback the migration."""
    op.alter_column(
        'products',
        'price',
        existing_type=sa.Numeric(precision=10, scale=2),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )
