"""added hint used column in users

Revision ID: 1bfcc06bb171
Revises: 6bcd5294b748
Create Date: 2024-10-19 13:44:17.306821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bfcc06bb171'
down_revision: Union[str, None] = '6bcd5294b748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hint_used', sa.PickleType(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'hint_used')
    # ### end Alembic commands ###