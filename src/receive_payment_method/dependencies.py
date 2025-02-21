from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from src.db.models import ReceiverPay


async def get_method_or_404(method_uid: str, session: AsyncSession = Depends(get_session)):
    method = await session.scalar(select(ReceiverPay).where(ReceiverPay.uid == method_uid))
    if method is None:
        raise HTTPException(status_code=404, detail="Method not found")
    return method