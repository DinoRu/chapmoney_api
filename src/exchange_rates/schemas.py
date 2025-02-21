from uuid import UUID

from pydantic import BaseModel
from pydantic.v1 import UUID1


class ExchangeRate(BaseModel):
	base: str
	to: str
	rate: float


class CreateRate(ExchangeRate):
	pass


class ViewRate(ExchangeRate):
	uid: UUID


class UpdateRate(BaseModel):
	base: str
	to: str
	rate: float