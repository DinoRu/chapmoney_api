from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import Country


async def get_country_or_404(country_uid: str, session: AsyncSession = Depends(get_session)):
    country = await session.scalar(select(Country).where(Country.uid == country_uid))
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country