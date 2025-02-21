from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.country.dependencies import get_country_or_404
from src.country.schemas import CountryView, CreateCountry, UpdateCountry
from src.country.service import CountryService
from src.db.main import get_session
from src.db.models import Country

country_router = APIRouter()
country_service = CountryService()
role_checker = Depends(RoleChecker(['admin']))


@country_router.get("/", response_model=list[CountryView],
					status_code=status.HTTP_200_OK)
async def get_countries(
		session: AsyncSession = Depends(get_session)
):
	countries = await country_service.get_countries(session)
	return countries


@country_router.get("/{country_uid}")
async def get_country(
		country: Country = Depends(get_country_or_404)
):
	return country


@country_router.post("/",
					 status_code=status.HTTP_201_CREATED,
					 response_model=CountryView,
					 dependencies=[role_checker]
					 )
async def create_country(
		country_data: CreateCountry,
		session: AsyncSession = Depends(get_session)
):
	country = await country_service.create_country(country_data, session)
	return country


@country_router.patch('/{country_uid}',
					  response_model=CountryView,
					  dependencies=[role_checker]
					  )
async def update_country(
		update_data: UpdateCountry,
		country: Country = Depends(get_country_or_404),
		session: AsyncSession = Depends(get_session)
):
	country_updated = await country_service.update_country(country, update_data, session)
	return country_updated


@country_router.delete("/{country_uid}", dependencies=[role_checker])
async def delete_country(
		country: Country = Depends(get_country_or_404),
		session: AsyncSession = Depends(get_session)
):
	country_to_delete = await country_service.delete_country(country, session)
	if country_to_delete is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Country not found"
		)
	else:
		return {}