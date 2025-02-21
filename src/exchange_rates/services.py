from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import ExchangeRate
from src.exchange_rates.schemas import CreateRate, UpdateRate


class RateService:

	async def get_rates(self, session: AsyncSession):
		query = select(ExchangeRate)
		result = await session.execute(query)
		rates = result.scalars().all()
		return rates

	async  def create_rate(self, rate: CreateRate, session: AsyncSession):
		rate_data = rate.model_dump()
		new_rate = ExchangeRate(**rate_data)

		session.add(new_rate)

		await session.commit()

		return new_rate

	async def update_rate(self, rate: ExchangeRate, rate_data: UpdateRate, session: AsyncSession):

		rate_data_dict = rate_data.dict(exclude_unset=True)
		for k, v in rate_data_dict.items():
			setattr(rate, k, v)
		await session.commit()
		await session.refresh(rate)

		return rate

	async def delete_rate(self, rate: ExchangeRate, session: AsyncSession):
		await session.delete(rate)
		await session.commit()
		return {
			"message": "Rate deleted successfully."
		}