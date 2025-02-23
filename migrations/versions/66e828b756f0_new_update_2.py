"""new update_2

Revision ID: 66e828b756f0
Revises: aa14bbefed05
Create Date: 2025-02-23 17:48:51.284248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '66e828b756f0'
down_revision: Union[str, None] = 'aa14bbefed05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('sender_country', sa.VARCHAR(), nullable=False))
    op.add_column('transactions', sa.Column('sending_method', sa.VARCHAR(), nullable=False))
    op.add_column('transactions', sa.Column('recipient_country', sa.VARCHAR(), nullable=False))
    op.add_column('transactions', sa.Column('receiving_method', sa.VARCHAR(), nullable=False))
    op.add_column('transactions', sa.Column('rate', sa.DECIMAL(precision=10, scale=6), nullable=False))
    op.add_column('transactions', sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True))
    op.alter_column('transactions', 'amount_sent',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.DECIMAL(precision=10, scale=6),
               existing_nullable=False)
    op.alter_column('transactions', 'amount_received',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.DECIMAL(precision=10, scale=6),
               existing_nullable=False)
    op.drop_column('transactions', 'source_country')
    op.drop_column('transactions', 'destination_country')
    op.drop_column('transactions', 'payment_method')
    op.drop_column('transactions', 'completed_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('transactions', sa.Column('payment_method', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('destination_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('source_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('transactions', 'amount_received',
               existing_type=sa.DECIMAL(precision=10, scale=6),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    op.alter_column('transactions', 'amount_sent',
               existing_type=sa.DECIMAL(precision=10, scale=6),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    op.drop_column('transactions', 'created_at')
    op.drop_column('transactions', 'rate')
    op.drop_column('transactions', 'receiving_method')
    op.drop_column('transactions', 'recipient_country')
    op.drop_column('transactions', 'sending_method')
    op.drop_column('transactions', 'sender_country')
    # ### end Alembic commands ###
