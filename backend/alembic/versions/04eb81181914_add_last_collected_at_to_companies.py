"""add last_collected_at to companies

Revision ID: 04eb81181914
Revises: 532517b98835
Create Date: 2026-03-26 23:40:46.685364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04eb81181914'
down_revision: Union[str, Sequence[str], None] = '532517b98835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("companies", sa.Column("last_collected_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("companies", "last_collected_at")
