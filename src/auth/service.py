from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_passwd_hash
from src.db.models import User


class UserService:

	

	async def get_user_by_email(self, email: str, session: AsyncSession):
		statement = select(User).where(User.email == email)
		result = await session.execute(statement)
		return result.scalar_one_or_none()

	async def user_exist(self, email, session: AsyncSession):
		user = await self.get_user_by_email(email, session)

		return True if user is not None else False

	async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
		user_data_dict = user_data.model_dump()

		new_user = User(**user_data_dict)
		new_user.password_hash = generate_passwd_hash(user_data_dict['password'])

		session.add(new_user)
		await session.commit()

		return new_user

	async def update_user(self, user: User, user_data: dict, session: AsyncSession):

		for k, v in user_data.items():
			setattr(user, k, v)

		await session.commit()
		await session.refresh(user)
		return user
