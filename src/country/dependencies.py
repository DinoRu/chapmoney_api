from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import Country


async def get_country_or_404(country_uid: str, session: AsyncSession = Depends(get_session)):
    country = await session.scalar(select(Country).where(Country.uid == country_uid))
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


async def get_country_currency(country_name: str, session: AsyncSession = Depends(get_session)):
    stmt = select(Country).where(Country.name == country_name)
    result = await session.execute(stmt)
    country = result.scalars().first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country '{country_name}' not found")
    return country.currency_code