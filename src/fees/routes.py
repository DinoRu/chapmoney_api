from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.db.models import Fee
from src.fees.dependencies import get_fee_or_404
from src.fees.schemas import FeeView, CreateFee, UpdateFee
from src.fees.services import FeeService

fee_router = APIRouter()

fee_service = FeeService()
role_checker = Depends(RoleChecker(['admin']))

@fee_router.get("/", response_model=list[FeeView])
async def get_all_fee(session: AsyncSession = Depends(get_session)):
	fees = await fee_service.get_fees(session)
	return fees


@fee_router.get("/{fee_uid}", response_model=FeeView)
async def get_fee(
		fee: Fee = Depends(get_fee_or_404),
):
	return fee


@fee_router.post("/",
				 response_model=FeeView,
				 status_code=status.HTTP_201_CREATED,
				 dependencies=[role_checker]
				 )
async def create_fee(
		fee_data: CreateFee,
		session: AsyncSession = Depends(get_session)
):
	new_fee = await fee_service.create_fee(fee_data, session)
	return new_fee


@fee_router.patch("/{fee_uid}",
				  response_model=FeeView,
				  dependencies=[role_checker]
				  )
async def fee_to_update(
		fee_data: UpdateFee,
		fee: Fee = Depends(get_fee_or_404),
		session: AsyncSession = Depends(get_session)
):
	fee_updated = await fee_service.update_fee(fee, fee_data, session)
	return fee_updated


@fee_router.delete("/{fee_id}",
				   dependencies=[role_checker])
async def fee_to_delete(
		fee: Fee = Depends(get_fee_or_404),
		session: AsyncSession = Depends(get_session)
):
	delete_fee = await fee_service.delete_fee(fee, session)
	if delete_fee is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Fee not found."
		)
	else:
		return {}