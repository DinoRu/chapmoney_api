from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.currency.dependencies import get_currency_or_404
from src.currency.schemas import CurrencyModel, CurrencyView, CreateCurrency, UpdateCurrency
from src.currency.services import CurrencyService
from src.db.main import get_session
from src.db.models import Currency

currency_router = APIRouter()
currency_service = CurrencyService()
role_checker = Depends(RoleChecker(["admin"]))


@currency_router.get("/",
					 response_model=list[CurrencyView]
					)
async def get_currencies(session: AsyncSession = Depends(get_session)):
	currencies = await currency_service.get_currencies(session)
	return currencies

@currency_router.get("/{currency_uid}", response_model=CurrencyView)
async def get_currency(
		currency: Currency = Depends(get_currency_or_404)
):
	return currency


@currency_router.post("/",
					  response_model=CurrencyView,
					  status_code=status.HTTP_201_CREATED,
					  dependencies=[role_checker])
async def create_currency(currency_data: CreateCurrency, session: AsyncSession = Depends(get_session)):
	new_currency = await currency_service.create_currency(currency_data, session)

	return new_currency


@currency_router.patch("/{currency_uid}", response_model=CurrencyView, dependencies=[role_checker])
async def currency_to_update(
		currency_data: UpdateCurrency,
		currency: Currency = Depends(get_currency_or_404),
		session: AsyncSession = Depends(get_session)
):
	currency_updated = await currency_service.update_currency(currency, currency_data, session)
	return currency_updated


@currency_router.delete('/{currency_uid}', dependencies=[role_checker])
async def delete_currency(
		currency: Currency = Depends(get_currency_or_404),
		session: AsyncSession = Depends(get_session)
):
	currency_to_delete = await currency_service.delete_currency(currency, session)
	if currency_to_delete is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Currency not Found."
		)
	else:
		return {}