import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Column, Relationship, DECIMAL
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    phone_number: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default='user'))
    pin: str = Field(sa_column=Column(pg.VARCHAR, nullable=True), exclude=True)
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    transactions: List['Transaction'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True
    )


class Currency(SQLModel, table=True):
    __tablename__ = "currencies"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    code: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    symbol: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    countries: List['Country'] = Relationship(
        back_populates='currency',
        sa_relationship_kwargs={'lazy': 'selectin'},
        cascade_delete=True
    )



class Country(SQLModel, table=True):
    __tablename__ = "countries"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    code: str = Field(sa_column=Column(pg.VARCHAR(4), unique=True, nullable=False))
    flag: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    currency_code: str = Field(foreign_key='currencies.code', ondelete='CASCADE')
    currency: Currency = Relationship(back_populates='countries')


    s_pays: List['SenderPay'] = Relationship(
        back_populates='country',
        sa_relationship_kwargs={'lazy': 'selectin'},
        cascade_delete=True
    )

    r_pays: List['ReceiverPay'] = Relationship(
        back_populates='country',
        sa_relationship_kwargs={'lazy': 'selectin'},
        cascade_delete=True
    )


class ExchangeRate(SQLModel, table=True):
    __tablename__ = 'exchange_rates'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    base: str = Field(foreign_key="currencies.code", nullable=False, ondelete='CASCADE')
    to: str = Field(foreign_key="currencies.code", nullable=False, ondelete='CASCADE')
    rate: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class Fee(SQLModel, table=True):
    __tablename__ = 'fees'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    base: str = Field(foreign_key='countries.name', nullable=False, ondelete='CASCADE')
    to: str = Field(foreign_key='countries.name', nullable=False, ondelete='CASCADE')
    fee: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class SenderPay(SQLModel, table=True):
    __tablename__ = "s_payments"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    method_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    sender_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    sender_phone: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    country_name: str = Field(foreign_key='countries.name', nullable=False, ondelete='CASCADE')
    country: Country = Relationship(back_populates='s_pays')


class ReceiverPay(SQLModel, table=True):
    __tablename__ = 'r_payments'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    method_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    country_name: str = Field(foreign_key="countries.name", nullable=False, ondelete='CASCADE')
    country: Country = Relationship(back_populates='r_pays')


class Transaction(SQLModel, table=True):
    __tablename__ = 'transactions'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    sender_id: Optional[uuid.UUID] = Field(foreign_key='users.uid', nullable=False)
    transaction_number: str = Field(sa_column=Column(pg.VARCHAR, unique=True, nullable=False),
                                    default_factory=lambda: f"TXN-{uuid.uuid4().hex[:10].upper()}")
    amount_sent: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    source_country: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    amount_received: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    destination_country: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    receiver_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    receiver_number: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    payment_method: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    status: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, default='Pending'))
    completed_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))
    user: User = Relationship(back_populates='transactions')


class Rate(SQLModel, table=True):
    __tablename__ = "rates"
    __table_args__ = (Index('idx_currency', 'currency'),)
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    currency: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, index=True))
    rate: Decimal = Field(sa_column=Column(DECIMAL(precision=10, scale=4), nullable=False))






