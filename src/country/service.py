from pytz import country_names
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.country.schemas import CreateCountry, UpdateCountry
from src.db.models import Country


class CountryService:

	async def get_countries(self, session: AsyncSession):
		query = select(Country)
		result = await session.execute(query)
		countries = result.scalars().all()
		return countries

	async def create_country(self, country_data: CreateCountry, session: AsyncSession):
		country_data_dict = country_data.model_dump(exclude_unset=True)
		country = Country(**country_data_dict)
		session.add(country)
		await session.commit()

		return country

	async def update_country(self, country: Country, country_data: UpdateCountry, session: AsyncSession):
		update_dict = country_data.model_dump(exclude_unset=True)

		for k, v in update_dict.items():
			setattr(country, k, v)
		await session.commit()
		await session.refresh(country)
		return country


	async def delete_country(self, country: Country, session: AsyncSession):
		await session.delete(country)
		await session.commit()
		return {}