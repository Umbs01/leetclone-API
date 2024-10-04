"""score -> points col in problems

Revision ID: b5afd22b18d1
Revises: b8beaff0299f
Create Date: 2024-10-04 14:31:24.120602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b5afd22b18d1'
down_revision: Union[str, None] = 'b8beaff0299f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problems', sa.Column('points', sa.Integer(), nullable=True))
    op.alter_column('problems', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('problems', 'score')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problems', sa.Column('score', sa.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('problems', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('problems', 'points')
    # ### end Alembic commands ###