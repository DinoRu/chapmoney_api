from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.db.models import ExchangeRate
from src.exchange_rates.dependencies import get_rate_or_404
from src.exchange_rates.schemas import ViewRate, CreateRate, UpdateRate
from src.exchange_rates.services import RateService

rate_router = APIRouter()
rate_service = RateService()
role_checker = Depends(RoleChecker(["admin"]))

@rate_router.get("/", response_model=list[ViewRate])
async def get_rates(
		session: AsyncSession = Depends(get_session)
):
	rates = await rate_service.get_rates(session)
	return rates


@rate_router.get("/{rate_uid}", response_model=ViewRate)
async def get_rate_404(
		rate: ExchangeRate = Depends(get_rate_or_404),
):
	return rate


@rate_router.post(
	"/create",
	status_code=status.HTTP_201_CREATED,
	response_model=ViewRate,
	dependencies=[role_checker]
)
async def create_rate(
		rate_data: CreateRate,
		session: AsyncSession = Depends(get_session),
):
	new_rate = await rate_service.create_rate(rate_data, session)
	return new_rate


@rate_router.patch("/{rate_uid}",
				   response_model=ViewRate,
				   dependencies=[role_checker])
async def update_rate(
		rate_data: UpdateRate,
		rate: ExchangeRate = Depends(get_rate_or_404),
		session: AsyncSession = Depends(get_session)
):
	rate_updated = await rate_service.update_rate(rate, rate_data, session)

	if rate_updated is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Rate not found."
		)
	return rate_updated


@rate_router.delete("/{rate_uid}", dependencies=[role_checker])
async def rate_to_delete(
		rate: ExchangeRate = Depends(get_rate_or_404),
		session: AsyncSession = Depends(get_session)
):
	rate_deleted = await rate_service.delete_rate(rate, session)
	if rate_deleted is not None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Rate not found."
		)
	else:
		return {}