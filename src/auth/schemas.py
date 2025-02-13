import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.transactions.schemas import Transaction


class UserCreateModel(BaseModel):
	first_name: str = Field(max_length=25)
	last_name: str = Field(max_length=25)
	email: str = Field(max_length=40)
	phone_number: str = Field(max_length=15)
	password: str = Field(min_length=6)

	model_config = {
		"json_schema_extra": {
			"example": {
				"first_name": "John",
				"last_name": "Doe",
				"email": "johndoe123@gmail.com",
				"phone_number": "+7 989 459 10 49",
				"password": "testpass123",
			}
		}
	}


class UserModel(BaseModel):
	uid: uuid.UUID
	email: str
	first_name: str
	last_name: str
	password_hash: str = Field(exclude=True)
	created_at: datetime
	update_at: datetime


class UserTransactionModel(UserModel):
	transactions: List[Transaction]


class UserLoginModel(BaseModel):
	email: str = Field(max_length=40)
	password: str = Field(min_length=6)


class EmailModel(BaseModel):
	addresses: List[str]


class PasswordResetRequestModel(BaseModel):
	email: str


class PasswordResetConfirmModel(BaseModel):
	new_password: str
	confirm_new_password: str
