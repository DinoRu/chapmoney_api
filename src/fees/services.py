from fastapi import HTTPException
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Fee
from src.fees.schemas import CreateFee, UpdateFee


class FeeService:

	async def get_fees(self, session: AsyncSession):
		query = select(Fee)
		result = await session.execute(query)
		fees = result.scalars().all()
		return fees

	async def create_fee(self, fee_data: CreateFee, session: AsyncSession):
		fee_data_dict = fee_data.model_dump()
		new_fee = Fee(**fee_data_dict)

		session.add(new_fee)
		await session.commit()
		return new_fee

	async def update_fee(self, fee: Fee, fee_data: UpdateFee, session: AsyncSession):
		update_fee_dict = fee_data.dict(exclude_unset=True)

		for k, v in update_fee_dict.items():
			setattr(fee, k, v)

		await session.commit()
		await session.refresh(fee)

		return fee

	async def delete_fee(self, fee: Fee, session: AsyncSession):
		await session.delete(fee)
		await session.commit()
		return {}

	async def get_fee_from_country(self, source_country: str, target_country: str, session: AsyncSession):
		stmt = select(Fee).where(Fee.base == source_country, Fee.to == target_country)
		result = await session.execute(stmt)
		fee = result.scalar_one_or_none()
		if fee is None:
			raise HTTPException(
				status_code=404,
				detail="Fee not found..."
			)
		print(fee)
		return fee