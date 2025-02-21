from fastapi.params import Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from src.db.main import get_session
from src.db.models import ExchangeRate


async def get_rate_or_404(rate_uid: str, session: AsyncSession = Depends(get_session)):
	query = select(ExchangeRate).where(ExchangeRate.uid == rate_uid)
	result = await session.exec(query)
	rate = result.scalar_one_or_none()

	if rate is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Rate not found."
		)
	return rate