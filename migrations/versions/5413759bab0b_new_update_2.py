"""new update_2

Revision ID: 5413759bab0b
Revises: 66e828b756f0
Create Date: 2025-02-23 20:30:15.325712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5413759bab0b'
down_revision: Union[str, None] = '66e828b756f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'amount_sent',
               existing_type=sa.NUMERIC(precision=10, scale=6),
               type_=sa.DECIMAL(precision=10, scale=4),
               existing_nullable=False)
    op.alter_column('transactions', 'amount_received',
               existing_type=sa.NUMERIC(precision=10, scale=6),
               type_=sa.DECIMAL(precision=10, scale=4),
               existing_nullable=False)
    op.alter_column('transactions', 'rate',
               existing_type=sa.NUMERIC(precision=10, scale=6),
               type_=sa.DECIMAL(precision=10, scale=4),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'rate',
               existing_type=sa.DECIMAL(precision=10, scale=4),
               type_=sa.NUMERIC(precision=10, scale=6),
               existing_nullable=False)
    op.alter_column('transactions', 'amount_received',
               existing_type=sa.DECIMAL(precision=10, scale=4),
               type_=sa.NUMERIC(precision=10, scale=6),
               existing_nullable=False)
    op.alter_column('transactions', 'amount_sent',
               existing_type=sa.DECIMAL(precision=10, scale=4),
               type_=sa.NUMERIC(precision=10, scale=6),
               existing_nullable=False)
    # ### end Alembic commands ###
