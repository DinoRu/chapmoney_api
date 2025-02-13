import uuid
from datetime import datetime

from pydantic import BaseModel

from src.auth.schemas import UserModel


class Transaction(BaseModel):
	uid: uuid.UUID
	amount: float
	amount_converted: float
	final_amount: float
	base_country: str
	target_country: str
	s_pay: str
	receiver_name: str
	receiver_number: str
	r_pay: str
	created_at: datetime
	updated_at: datetime

class TransactionDetailModel(Transaction):
	user: UserModel


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



