"""Added initial table

Revision ID: 9f0fdb960de9
Revises: 
Create Date: 2023-09-20 00:18:05.643108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f0fdb960de9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'levels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('filename', sa.String(), nullable=True, unique=True),
        sa.Column('matrix', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('bonus_words', sa.JSON(), nullable=True),
        sa.Column('words', sa.JSON(), nullable=False)
    )
    op.create_table(
        'words',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('word', sa.String(), nullable=False, unique=True)
    )


def downgrade() -> None:
    op.drop_table('words')
    op.drop_table('levels')
