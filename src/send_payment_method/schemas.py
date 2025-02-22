import uuid

from pydantic import BaseModel

class SenderPaymentModel(BaseModel):
	method_name: str
	sender_name: str
	sender_phone: str
	country_name: str

class CreateSenderPaymentMethod(SenderPaymentModel):
	pass

class UpdateSenderPaymentMethod(SenderPaymentModel):
	pass

class SenderPaymentView(SenderPaymentModel):
	uid: uuid.UUID