from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.db.models import ReceiverPay
from src.receive_payment_method.dependencies import get_method_or_404
from src.receive_payment_method.schemas import RMethodView, CreateRMethod, UpdateRMethod
from src.receive_payment_method.service import RMethodService

r_method_router = APIRouter()
r_method_service = RMethodService()
role_checker = Depends(RoleChecker(['admin']))


@r_method_router.get("/", response_model=list[RMethodView], status_code=status.HTTP_200_OK)
async def get_methods(session: AsyncSession = Depends(get_session)):
	methods = await r_method_service.get_methods(session)

	return methods


@r_method_router.get("/{method_uid}", response_model=RMethodView, status_code=status.HTTP_200_OK)
async def get_method(
		method: ReceiverPay = Depends(get_method_or_404)
):
	return method


@r_method_router.post("/", response_model=RMethodView, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_method(
		method_data: CreateRMethod,
		session: AsyncSession = Depends(get_session)
):
	method = await r_method_service.create_method(session, method_data)
	return method


@r_method_router.patch("/{method_uid}", response_model=RMethodView, dependencies=[role_checker])
async def update_method(
		update_data: UpdateRMethod,
		method: ReceiverPay = Depends(get_method_or_404),
		session: AsyncSession = Depends(get_session)
):
	method_to_update = await r_method_service.update_method(method, update_data, session)
	return method_to_update


@r_method_router.delete("/{method_uid}", dependencies=[role_checker])
async def delete_method(
		method: ReceiverPay = Depends(get_method_or_404),
		session: AsyncSession = Depends(get_session)
):
	method_to_delete = await r_method_service.delete_method(session, method)
	if method_to_delete is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found")
	return {}