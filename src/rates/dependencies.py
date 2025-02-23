from typing import Dict, Any
from decimal import Decimal, localcontext

from celery.bin.result import result
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config
from src.country.dependencies import get_country_currency
from src.db.main import get_session
from src.db.models import Rate
from src.rates.schema import ExchangeRates


async def get_rate_or_404(rate_uid: str, session: AsyncSession = Depends(get_session)):
	query = select(Rate).where(Rate.uid == rate_uid)
	result = await session.exec(query)
	rate = result.scalar_one_or_none()

	if rate is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Rate not found."
		)
	return rate

async def get_all_rates(session: AsyncSession = Depends(get_session)):
	query = select(Rate).order_by(Rate.currency)
	result = await session.execute(query)
	exchange_rates = result.scalars().all()
	rates = {rate.currency: rate.rate for rate in exchange_rates}

	return rates

async def get_rate(
		base: str,
		to: str,
		rates: Dict[str, Any] = Depends(get_all_rates)
) -> ExchangeRates:
	with localcontext() as ctx:
		ctx.prec = 2 * Config.DECIMAL_PRECISION
		current_rate = rates[to] / rates[base]
	current_rate = round(current_rate, Config.DECIMAL_PRECISION)
	return ExchangeRates(quote=current_rate)


async def get_rate_by_country(
		sender_country: str =  Depends(lambda: Path(...)),
		recipient_country: str =  Depends(lambda: Path(...)),
		session: AsyncSession = Depends(get_session)
) -> ExchangeRates:
	exchange_rates = await  get_all_rates(session)
	base_currency = await get_country_currency(sender_country, session)
	target_currency = await get_country_currency(recipient_country, session)
	with localcontext() as ctx:
		ctx.prec = 2 * Config.DECIMAL_PRECISION
		current_rate = exchange_rates[target_currency] / exchange_rates[base_currency]
	current_rate = round(current_rate, Config.DECIMAL_PRECISION)
	return ExchangeRates(quote=current_rate)


async def convert_currencies(
		amount: Decimal,
		rate: ExchangeRates = Depends(get_rate_by_country)
) -> Decimal:
	with localcontext() as ctx:
		ctx.prec = 2 * Config.DECIMAL_PRECISION
		result = rate.quote * amount
	return round(result, Config.DECIMAL_PRECISION)