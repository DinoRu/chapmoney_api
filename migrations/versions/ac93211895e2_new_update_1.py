"""new update_1

Revision ID: ac93211895e2
Revises: e665b7477035
Create Date: 2025-02-21 17:44:26.145583

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac93211895e2'
down_revision: Union[str, None] = 'e665b7477035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange_rates', sa.Column('base', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('exchange_rates', sa.Column('to', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_constraint('exchange_rates_target_currency_fkey', 'exchange_rates', type_='foreignkey')
    op.drop_constraint('exchange_rates_base_currency_fkey', 'exchange_rates', type_='foreignkey')
    op.create_foreign_key(None, 'exchange_rates', 'currencies', ['to'], ['code'], ondelete='CASCADE')
    op.create_foreign_key(None, 'exchange_rates', 'currencies', ['base'], ['code'], ondelete='CASCADE')
    op.drop_column('exchange_rates', 'target_currency')
    op.drop_column('exchange_rates', 'base_currency')
    op.add_column('fees', sa.Column('base', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('fees', sa.Column('to', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('fees', sa.Column('fee', sa.FLOAT(), nullable=False))
    op.drop_constraint('fees_target_country_fkey', 'fees', type_='foreignkey')
    op.drop_constraint('fees_base_country_fkey', 'fees', type_='foreignkey')
    op.create_foreign_key(None, 'fees', 'countries', ['to'], ['name'], ondelete='CASCADE')
    op.create_foreign_key(None, 'fees', 'countries', ['base'], ['name'], ondelete='CASCADE')
    op.drop_column('fees', 'target_country')
    op.drop_column('fees', 'fees')
    op.drop_column('fees', 'base_country')
    op.add_column('transactions', sa.Column('sender_id', sa.Uuid(), nullable=False))
    op.add_column('transactions', sa.Column('amount_sent', sa.FLOAT(), nullable=False))
    op.add_column('transactions', sa.Column('source_country', sa.VARCHAR(), nullable=False))
    op.add_column('transactions', sa.Column('amount_received', sa.FLOAT(), nullable=False))
    op.add_column('transactions', sa.Column('destination_country', sa.VARCHAR(), nullable=False))
    op.drop_constraint('transactions_base_country_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_user_id_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_target_country_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'users', ['sender_id'], ['uid'])
    op.drop_column('transactions', 'target_country')
    op.drop_column('transactions', 'receive_amount')
    op.drop_column('transactions', 'transfer_amount')
    op.drop_column('transactions', 'base_country')
    op.drop_column('transactions', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('base_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('transfer_amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('receive_amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('target_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_target_country_fkey', 'transactions', 'countries', ['target_country'], ['name'])
    op.create_foreign_key('transactions_user_id_fkey', 'transactions', 'users', ['user_id'], ['uid'])
    op.create_foreign_key('transactions_base_country_fkey', 'transactions', 'countries', ['base_country'], ['name'])
    op.drop_column('transactions', 'destination_country')
    op.drop_column('transactions', 'amount_received')
    op.drop_column('transactions', 'source_country')
    op.drop_column('transactions', 'amount_sent')
    op.drop_column('transactions', 'sender_id')
    op.add_column('fees', sa.Column('base_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('fees', sa.Column('fees', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('fees', sa.Column('target_country', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'fees', type_='foreignkey')
    op.drop_constraint(None, 'fees', type_='foreignkey')
    op.create_foreign_key('fees_base_country_fkey', 'fees', 'countries', ['base_country'], ['name'], ondelete='CASCADE')
    op.create_foreign_key('fees_target_country_fkey', 'fees', 'countries', ['target_country'], ['name'], ondelete='CASCADE')
    op.drop_column('fees', 'fee')
    op.drop_column('fees', 'to')
    op.drop_column('fees', 'base')
    op.add_column('exchange_rates', sa.Column('base_currency', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('exchange_rates', sa.Column('target_currency', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'exchange_rates', type_='foreignkey')
    op.drop_constraint(None, 'exchange_rates', type_='foreignkey')
    op.create_foreign_key('exchange_rates_base_currency_fkey', 'exchange_rates', 'currencies', ['base_currency'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('exchange_rates_target_currency_fkey', 'exchange_rates', 'currencies', ['target_currency'], ['code'], ondelete='CASCADE')
    op.drop_column('exchange_rates', 'to')
    op.drop_column('exchange_rates', 'base')
    # ### end Alembic commands ###
