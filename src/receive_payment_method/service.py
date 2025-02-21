from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import ReceiverPay
from src.receive_payment_method.schemas import CreateRMethod, UpdateRMethod


class RMethodService:

	async def get_methods(self, session: AsyncSession):
		query = select(ReceiverPay)
		result = await session.execute(query)
		methods = result.scalars().all()

		return methods

	async def create_method(self, session: AsyncSession, method_data: CreateRMethod):
		method_data_dict = method_data.model_dump()

		method = ReceiverPay(**method_data_dict)

		session.add(method)
		await session.commit()

		return method

	async def update_method(self, method: ReceiverPay, update_data: UpdateRMethod, session:AsyncSession):

		method_data_dict = update_data.model_dump(exclude_unset=True)
		for k, v in method_data_dict.items():
			setattr(method, k, v)

		await session.commit()
		await session.refresh(method)

		return method

	async def delete_method(self, session: AsyncSession, method: ReceiverPay):
		await session.delete(method)
		await session.commit()
		return {}