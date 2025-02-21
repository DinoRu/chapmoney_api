from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from src.db.models import Currency


async def get_currency_or_404(currency_uid: str, session: AsyncSession = Depends(get_session)):
	query = select(Currency).where(Currency.uid == currency_uid)
	result = await session.execute(query)
	currency = result.scalar_one_or_none()
	return currency