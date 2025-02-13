import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, Relationship
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
        sa_relationship_args={'lazy': 'selectin'},
        cascade_delete=True
    )


class Currency(SQLModel, table=True):
    __tablename__ = "currencies"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    code: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    symbol: str
    full_name: str
    countries: List['Country'] = Relationship(
        back_populates='currency',
        sa_relationship_args={'lazy': 'selectin'},
        cascade_delete=True
    )



class Country(SQLModel, table=True):
    __tablename__ = "countries"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    code: str = Field(sa_column=Column(pg.VARCHAR(4), unique=True, nullable=False))
    flag: str
    currency_code: str = Field(foreign_key='currencies.code')
    currency: Currency = Relationship(back_populates='countries')
    s_pays: List['SenderPay'] = Relationship(
        back_populates='country',
        sa_relationship_args={'lazy': 'selectin'},
        cascade_delete=True
    )
    r_pays: List['ReceiverPay'] = Relationship(
        back_populates='country',
        sa_relationship_args={'lazy': 'selectin'},
        cascade_delete=True
    )


class ExchangeRate(SQLModel, table=True):
    __tablename__ = 'exchange_rates'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    base_currency: str = Field(foreign_key="currencies.code", nullable=False)
    target_currency: str = Field(foreign_key="currencies.code", nullable=False)
    rate: float
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class Fee(SQLModel, table=True):
    __tablename__ = 'fees'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    base_country: str = Field(foreign_key='countries.name', nullable=False)
    target_country: str = Field(foreign_key='countries.name', nullable=False)
    fees: float
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class SenderPay(SQLModel, table=True):
    __tablename__ = "s_payments"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    s_name: str
    sender_name: str
    sender_phone: str
    country_name: str = Field(foreign_key='countries.name', nullable=False)
    country: Country = Relationship(back_populates='s_pays')


class ReceiverPay(SQLModel, table=True):
    __tablename__ = 'r_payments'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    r_name: str
    country_name: str = Field(foreign_key="countries.name", nullable=False)
    country: Country = Relationship(back_populates='r_pays')


class Transaction(SQLModel, table=True):
    __tablename__ = 'transactions'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    amount: float
    amount_converted: float
    final_amount: float
    user_id: Optional[uuid.UUID] = Field(foreign_key='users.uid', nullable=False)
    base_country: str = Field(foreign_key='countries.name', nullable=False)
    target_country: str = Field(foreign_key='countries.name', nullable=False)
    s_pay: str
    receiver_name: str
    receiver_number: str
    r_pay: str
    status: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, default='Pending'))
    completed_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))
    user: User = Relationship(back_populates='transactions')





