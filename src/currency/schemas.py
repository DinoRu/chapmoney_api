import uuid

from pydantic import BaseModel

class CurrencyModel(BaseModel):
	code: str
	symbol: str


class CreateCurrency(CurrencyModel):
	pass


class UpdateCurrency(CurrencyModel):
	pass


class CurrencyView(CurrencyModel):
	uid: uuid.UUID