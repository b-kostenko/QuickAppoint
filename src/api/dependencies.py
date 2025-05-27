from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.database.postgres import get_db_session
from src.services.auth_service import auth_service

http_bearer = HTTPBearer()


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
        session: AsyncSession = Depends(get_db_session)
) -> User:
    try:
        return await auth_service.get_current_user(
            token=token.credentials, session=session
        )
    except HTTPException as e:
        raise e


async_session_dep = Annotated[AsyncSession, Depends(get_db_session)]
current_user_dep = Annotated[User, Depends(get_current_user)]