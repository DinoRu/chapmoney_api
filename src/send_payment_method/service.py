from fastapi import Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import SenderPay
from src.send_payment_method.schemas import CreateSenderPaymentMethod, UpdateSenderPaymentMethod


class SenderPayService:

	async def get_methods(self, session:AsyncSession = Depends(get_session)):
		query = select(SenderPay)
		result = await session.execute(query)
		payment_methods = result.scalars().all()
		return payment_methods

	async def create(self, method_data: CreateSenderPaymentMethod, session: AsyncSession):
		method_data_dict = method_data.model_dump(exclude_unset=True)

		method = SenderPay(**method_data_dict)
		session.add(method)

		await session.commit()

		return method

	async def update_method(self, method: SenderPay, update_data: UpdateSenderPaymentMethod, session: AsyncSession):
		update_data_dict = update_data.model_dump(exclude_unset=True)

		for k, v in update_data_dict.items():
			setattr(method, k, v)

		await session.commit()
		await session.refresh(method)

		return method

	async def delete_method(self, method: SenderPay, session: AsyncSession):
		await session.delete(method)
		await session.commit()
		return {}