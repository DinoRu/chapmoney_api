import uuid

from pydantic import BaseModel


class CountryModel(BaseModel):
	name: str
	code: str
	flag: str
	currency_code: str


class CreateCountry(CountryModel):
	pass


class UpdateCountry(BaseModel):
	name: str
	code: str
	flag: str
	currency_code: str


class CountryView(CountryModel):
	uid: uuid.UUID