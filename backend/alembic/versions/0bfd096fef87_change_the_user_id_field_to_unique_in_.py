"""change the user_id field to unique in Onboarding table

Revision ID: 0bfd096fef87
Revises: bca8b8d781c8
Create Date: 2024-08-21 16:46:29.577815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bfd096fef87'
down_revision: Union[str, None] = 'bca8b8d781c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'onboarding', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'onboarding', type_='unique')
    # ### end Alembic commands ###
