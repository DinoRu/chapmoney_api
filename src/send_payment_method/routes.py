
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.db.models import SenderPay
from src.send_payment_method.dependencies import get_payment_method_or_404
from src.send_payment_method.schemas import SenderPaymentView, CreateSenderPaymentMethod, UpdateSenderPaymentMethod
from src.send_payment_method.service import SenderPayService

sender_router = APIRouter()
sender_service = SenderPayService()
role_checker = Depends(RoleChecker(["admin"]))

@sender_router.get("/",
				   status_code=status.HTTP_200_OK,
				   response_model=list[SenderPaymentView])
async def get_all_methods(
		session: AsyncSession = Depends(get_session)
):
	methods = await sender_service.get_methods(session)
	return methods

@sender_router.get("/{method_uid}", response_model=SenderPaymentView)
async def get_method(
		method: SenderPay = Depends(get_payment_method_or_404)
):
	return method
#
@sender_router.post("/",
					response_model=SenderPaymentView,
					dependencies=[role_checker]
					)
async def create_method(
		method_data: CreateSenderPaymentMethod,
		session: AsyncSession = Depends(get_session)
):
	method = await sender_service.create(method_data, session)
	return method


@sender_router.patch("/{method_uid}",
					 response_model=SenderPaymentView,
					 dependencies=[role_checker]
					 )
async def update_method(
		update_data: UpdateSenderPaymentMethod,
		method: SenderPay = Depends(get_payment_method_or_404),
		session: AsyncSession = Depends(get_session)
):
	method = await sender_service.update_method(method, update_data, session)
	return method


@sender_router.delete("/{method_uid}",
					  dependencies=[role_checker])
async def delete_method(
		method: SenderPay = Depends(get_payment_method_or_404),
		session: AsyncSession = Depends(get_session)
):
	method_to_delete = await sender_service.delete_method(method, session)
	if method_to_delete is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Method is not found.')
	else:
		return {}