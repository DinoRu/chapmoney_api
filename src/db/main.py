from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))
Session = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)

async def get_session() -> AsyncGenerator:
	async with Session() as session:
		yield session


