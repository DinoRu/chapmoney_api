from fastapi import Depends
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
	return fee