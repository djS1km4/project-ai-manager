"""Change budget column from Integer to Float

Revision ID: c5affa85a0f2
Revises: 
Create Date: 2025-09-26 19:34:50.919790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5affa85a0f2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite doesn't support ALTER COLUMN TYPE, so we need to recreate the table
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('budget',
                   existing_type=sa.INTEGER(),
                   type_=sa.Float(),
                   existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite doesn't support ALTER COLUMN TYPE, so we need to recreate the table
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('budget',
                   existing_type=sa.Float(),
                   type_=sa.INTEGER(),
                   existing_nullable=True)
