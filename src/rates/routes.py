from decimal import Decimal
from typing import Dict, Any

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import Rate
from src.rates.dependencies import get_rate, convert_currencies
from src.rates.schema import ExchangeRateRequest, ConvertResponseModel, ExchangeRates

exchange_router = APIRouter()

@exchange_router.post("/exchange-rate")
async def add_exchange_rate(data: ExchangeRateRequest, session: AsyncSession = Depends(get_session)):
	for currency, rate in data.conversion_rates.items():
		query = select(Rate).where(Rate.currency == currency)
		result = await session.execute(query)
		existing_rate = result.scalar_one_or_none()
		if existing_rate:
			existing_rate.rate = rate  # Mise à jour
		else:
			rates = Rate(currency=currency, rate=rate)
			session.add(rates)
	await session.commit()
	return {"message": "Taux ajoutés avec succès"}


@exchange_router.get("/rates",
					 status_code=status.HTTP_200_OK
					 )
async def get_exchange_rates(session: AsyncSession = Depends(get_session)):
	query = select(Rate).order_by(Rate.currency)
	result = await session.execute(query)
	rates = result.scalars().all()
	print(rates)
	return {
		"response": "Success",
		"base_code": "USD",
		"conversion_rates": {rate.currency: rate.rate for rate in rates}
	}


@exchange_router.get("/{base}/{to}/{amount}", response_model=ConvertResponseModel)
async def convert(
		base: str = Path(...,
						 title="Base currency",
						 description="Base currency for conversion",
						 ),
		to: str = Path(...,
								 title="Target currency",
								 description="Target currency for conversion",
								 ),
		amount: Decimal = Path(
			...,
			gt=0,
			title="Amount of money",
			description="Amount of money that going to converted"
		),
		rates: ExchangeRates = Depends(get_rate),
		result: Decimal = Depends(convert_currencies)
) -> Dict[str, Any]:
	return {
		"base": base,
		"to": to,
		"amount": amount,
		"rates": rates,
		"result": result
	}