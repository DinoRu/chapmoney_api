import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Transaction(BaseModel):
	uid: uuid.UUID
	amount: float
	amount_converted: float
	final_amount: float
	base_country: str
	target_country: str

	receiver_name: str
	receiver_number: str
	r_pay: str
	created_at: datetime
	updated_at: datetime



class TransactionRequest(BaseModel):
	sending_method: str
	receiver_name: str
	receiver_number: str
	receiving_method: str


class TransactionClientResponse(BaseModel):
	uid: uuid.UUID
	transaction_number: str
	sender_country: str
	recipient_country: str
	amount_sent: Decimal
	amount_received: Decimal
	rate: Decimal
	sending_method: str
	receiver_name: str
	receiver_number: str
	receiving_method: str
	status: str
	created_at: datetime


class TransactionAdminResponse(BaseModel):
	uid: uuid.UUID
	transaction_number: str
	sender_name: str
	sender_number: str
	sender_country: str
	recipient_country: str
	amount_sent: Decimal
	amount_received: Decimal
	rate: Decimal
	sending_method: str
	receiver_name: str
	receiver_number: str
	receiving_method: str
	status: str
	created_at: datetime


class TransactionDetailModel(Transaction):
	user: "UserModel"


class TransactionCreateModel(BaseModel):
	amount: float
	base_country: str
	target_country: str
	s_pay: str
	receiver_name: str
	receiver_number: str
	r_pay: str

class TransactionUpdateModel(BaseModel):
	status: str



