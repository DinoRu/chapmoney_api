from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.currency.schemas import CreateCurrency, UpdateCurrency
from src.db.models import Currency


class CurrencyService:

	async def get_currencies(self, session: AsyncSession):
		query = select(Currency)
		result = await session.execute(query)
		currencies = result.scalars().all()
		return currencies

	async def create_currency(self, currency_data: CreateCurrency, session: AsyncSession):
		currency_data_dict = currency_data.model_dump(exclude_unset=True)
		new_currency = Currency(**currency_data_dict)

		session.add(new_currency)
		await session.commit()

		return new_currency

	async def update_currency(self, currency: Currency, currency_data: UpdateCurrency, session: AsyncSession):
		currency_data_dict = currency_data.model_dump(exclude_unset=True)

		for k, v in currency_data_dict.items():
			setattr(currency, k, v)
		await session.commit()
		await session.refresh(currency)

		return currency

	async def delete_currency(self, currency: Currency, session: AsyncSession):
		await session.delete(currency)
		await session.commit()
		return {}