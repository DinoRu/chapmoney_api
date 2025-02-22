from decimal import Decimal

from pydantic import BaseModel


class ExchangeRateRequest(BaseModel):
	base_code: str
	conversion_rates: dict

class ExchangeRates(BaseModel):
	quote: Decimal


class ConvertRequestModel(BaseModel):
	base: str
	to: str
	amount: Decimal


class ConvertResponseModel(BaseModel):
	base: str
	to: str
	amount: Decimal
	rates: ExchangeRates
	result: Decimal
