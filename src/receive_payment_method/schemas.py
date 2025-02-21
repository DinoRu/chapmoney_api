import uuid

from pydantic import BaseModel

class RMethodModel(BaseModel):
	method_name: str
	country_name: str


class CreateRMethod(RMethodModel):
	pass

class UpdateRMethod(RMethodModel):
	pass

class RMethodView(RMethodModel):
	uid: uuid.UUID