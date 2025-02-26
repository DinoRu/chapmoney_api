from decimal import Decimal

from fastapi import APIRouter, status, Path, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.fees.dependencies import get_fee_from_to
from src.fees.schemas import FeeView
from src.rates.schema import ExchangeRates
from src.websocket_manager import websocket_manager
from src.auth.dependencies import get_current_user
from src.db.main import get_session
from src.db.models import Transaction, User
from src.rates.dependencies import convert_currencies, get_rate_by_country
from src.transactions.schemas import TransactionRequest, TransactionClientResponse, TransactionAdminResponse

T_router = APIRouter()


async def get_rate_for_transaction(
    sender_country: str,
    recipient_country: str,
    rate: Decimal = Depends(get_rate_by_country),
) -> Decimal:
    return rate


async def get_transaction(transaction_uid: str, session: AsyncSession = Depends(get_session)):
    stmt = select(Transaction).where(Transaction.uid == transaction_uid)
    result = await session.execute(stmt)
    transaction = result.scalar_one_or_none()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return transaction


@T_router.post("/transaction/{sender_country}/{recipient_country}/{amount}",
               status_code=status.HTTP_201_CREATED,
               response_model=TransactionClientResponse
               )
async def create_transaction(
        transaction_data: TransactionRequest,
        sender_country: str = Path(
            ...,
            title="Sender country",
            description="The country which from where you send."
        ),
        recipient_country: str = Path(
            ...,
            title="Destination country",
            description="Country to receive the amount."
        ),
        amount: Decimal = Path(
            ...,
            title="Amount",
            description="The amount to send"
        ),
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    rate = await get_rate_by_country(sender_country, recipient_country, session=session)
    result = await convert_currencies(amount, rate)

    new_transaction = Transaction(
        sender_country=sender_country,
        recipient_country=recipient_country,
        amount_sent=amount,
        sender_id=user.uid,
        amount_received=result,
        sending_method=transaction_data.sending_method,
        receiver_name=transaction_data.receiver_name,
        receiver_number=transaction_data.receiver_number,
        receiving_method=transaction_data.receiving_method,
        rate=rate.quote,
        status="Pending",
    )

    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    await websocket_manager.send_to_admins(
        f"Nouvelle transaction en attente: {new_transaction.amount_sent} {new_transaction.sender_country} de {user.first_name}")

    return TransactionClientResponse(
        uid=new_transaction.uid,
        transaction_number=new_transaction.transaction_number,
        sender_country=new_transaction.sender_country,
        recipient_country=new_transaction.recipient_country,
        amount_sent=new_transaction.amount_sent,
        amount_received=new_transaction.amount_received,
        receiver_name=new_transaction.receiver_name,
        receiver_number=new_transaction.receiver_number,
        sending_method=new_transaction.sending_method,
        receiving_method=new_transaction.receiving_method,
        rate=new_transaction.rate,
        status=new_transaction.status,
        created_at=new_transaction.created_at
    )

@T_router.get("/client/transactions/{user_uid}",
              status_code=status.HTTP_200_OK,
              response_model=list[TransactionClientResponse])
async def get_client_transaction(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(Transaction).where(Transaction.sender_id == user.uid)
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    return transactions



@T_router.get(
    "/admin/transactions",
    status_code=status.HTTP_200_OK,
    response_model=list[TransactionAdminResponse]
)
async def get_all_transactions(
        session: AsyncSession = Depends(get_session),
):
    try:
        stmt = (
            select(Transaction, User)
            .join(User, User.uid == Transaction.sender_id)
        )
        result = await session.execute(stmt)
        transactions_with_users = result.all()
        return [
            TransactionAdminResponse(
                uid=t.uid,
                transaction_number=t.transaction_number,
                sender_name=u.first_name,
                sender_number=u.phone_number,
                sender_country=t.sender_country,
                sending_method=t.sending_method,
                amount_sent=t.amount_sent,
                amount_received=t.amount_received,
                rate=t.rate,
                receiver_name=t.receiver_name,
                receiver_number=t.receiver_number,
                recipient_country=t.recipient_country,
                receiving_method=t.receiving_method,
                status=t.status,
                created_at=t.created_at
            ) for t, u in transactions_with_users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@T_router.patch("/admin/transactions/{transaction_uid}/approve",
                status_code=status.HTTP_200_OK,
                response_model=TransactionClientResponse)
async def approve_transaction(
        session: AsyncSession = Depends(get_session),
        transaction: Transaction = Depends(get_transaction)
):
   transaction.status = "approved"
   await session.commit()
   await session.refresh(transaction)
   await websocket_manager.send_to_client(str(transaction.sender_id),
                                          f"Votre transaction de {transaction.amount_sent} {transaction.sender_country} a été approuvée!")
   return transaction


@T_router.get("/calculate-transfer/{sender_country}/{recipient_country}/{amount}", status_code=status.HTTP_200_OK)
async def calculate_transfer(
        sender_country: str = Path(
            ...,
            title="Source country",
            description="Source country to send."
        ),
        recipient_country: str = Path(
            ...,
            title="Target country",
            description="Target country to receive."
        ),
        amount: Decimal = Path(
            ...,
            title="Amount to send",
            description="Amount that you to send"
        ),
        session: AsyncSession = Depends(get_session)
):
    fee = await get_fee_from_to(sender_country, recipient_country, session)
    rate = await get_rate_by_country(sender_country, recipient_country, session)
    send_fee = amount * fee.fee
    total_amount = amount + send_fee

    converted_amount = amount * rate.quote

    return {
        "exchange_rate": rate.quote,
        "send_fee": send_fee,
        "total_amount_to_pay": total_amount,
        "amount_received": converted_amount
    }
