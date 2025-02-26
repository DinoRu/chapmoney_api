from decimal import Decimal

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select

from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import Fee


async def get_fee_or_404(
		fee_uid: str,
		session: AsyncSession = Depends(get_session)
):
	query = select(Fee).where(Fee.uid == fee_uid)
	result = await session.execute(query)
	fee = result.scalar_one_or_none()
	print(fee)
	return fee

async def get_fee_from_to(
		sender_country: str,
		recipient_country: str,
		session: AsyncSession = Depends(get_session)
) -> Decimal:
	stmt = select(Fee).where(Fee.base == sender_country, Fee.to == recipient_country)
	result = await session.execute(stmt)
	fees = result.scalar_one_or_none()
	if fees is None:
		raise HTTPException(status_code=404, detail="Fee not found.")
	return fees


