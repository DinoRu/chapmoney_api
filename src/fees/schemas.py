import uuid

from pydantic import BaseModel

class FeeModel(BaseModel):
	base: str
	to: str
	fee: float


class CreateFee(FeeModel):
	pass

class UpdateFee(BaseModel):
	fee: float

class FeeView(FeeModel):
	uid: uuid.UUID
