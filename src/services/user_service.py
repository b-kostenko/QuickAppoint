from typing import List

from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserResponse, UserSchema, UserUpdateSchema
from src.utils.exceptions import UserNotFoundExceptions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self):
        self.user_repository: UserRepository = UserRepository()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(secret=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(secret=plain_password, hash=hashed_password)

    async def create_user(self, user_input: UserSchema, session: AsyncSession) -> UserResponse:
        user_input.password = self.get_password_hash(user_input.password)

        user = await self.user_repository.create_user(user_input=user_input, session=session)
        logger.info(f"User has been created successfully with UUID: {user.uuid}")
        return UserResponse(
            uuid=str(user.uuid),
            username=user.username,
            email=user.email
        )

    async def get_users(self, session: AsyncSession) -> List[UserResponse]:
        users = await self.user_repository.get_users(session=session)
        if not users:
            return []
        return [UserResponse(
            uuid=str(user.uuid),
            username=user.username,
            email=user.email
        ) for user in users]

    async def get_user_by_email(self, email: str, session: AsyncSession) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email=email, session=session)
        if not user:
            raise UserNotFoundExceptions(email=email)
        return UserResponse(
            uuid=str(user.uuid),
            username=user.username,
            email=user.email
        )
    async def retrieve_user_info_by_email(self, email: str, session: AsyncSession) -> UserSchema:
        user = await self.user_repository.get_user_by_email(email=email, session=session)
        if not user:
            raise UserNotFoundExceptions(email=email)
        return UserSchema(
            uuid=str(user.uuid),
            username=user.username,
            email=user.email,
            password=user.password
        )

    async def update_user(self, user: User, user_input: UserUpdateSchema, session: AsyncSession) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email=user.email, session=session)
        user = await self.user_repository.update_user(user=user, user_input=user_input, session=session)
        return UserResponse(
            uuid=str(user.uuid),
            username=user.username,
            email=user.email
        )

    async def delete_user(self, user: User, session: AsyncSession) -> None:
        user = await self.user_repository.get_user_by_email(email=user.email, session=session)
        await self.user_repository.delete_user(user=user, session=session)



user_service = UserService()
