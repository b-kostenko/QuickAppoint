from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.schemas.users import UserSchema, UserUpdateSchema
from src.utils.exceptions import UserAlreadyExistsException


class UserRepository:

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_input: UserSchema, session: AsyncSession) -> User:
        existing_user = await self.get_user_by_email(user_input.email, session)
        if existing_user:
            raise UserAlreadyExistsException(email=user_input.email)

        user = User(**user_input.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_users(self, session: AsyncSession) -> List[User]:
        users = await session.execute(select(User))
        return list(users.scalars().all())

    async def update_user(self, user: User, user_input: UserUpdateSchema, session: AsyncSession) -> User:
        for key, value in user_input.model_dump().items():
            if value is not None:
                setattr(user, key, value)

        await session.commit()
        await session.refresh(user)

    async def delete_user(self, user: User, session: AsyncSession) -> None:
        await session.delete(user)
        await session.commit()
