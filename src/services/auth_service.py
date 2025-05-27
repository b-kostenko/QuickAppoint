from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models.users import User
from src.schemas.token import TokenSchema
from src.services.user_service import user_service
from src.settings import settings
from src.utils.exceptions import UserNotFoundExceptions


class AuthService:

    def _decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.token.SECRET_KEY, algorithms=[settings.token.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def _encode_access_token(self, payload: Dict, access_token_expire_minutes: int) -> str:
        to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.token.SECRET_KEY, algorithm=settings.token.ALGORITHM)
        return encoded_jwt


    def login_for_access_token(self, user: User) -> TokenSchema:
        access_token_expires = settings.token.ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = self._encode_access_token(
            payload={"email": user.email},
            access_token_expire_minutes=access_token_expires
        )
        return TokenSchema(
            access_token=access_token,
            token_type=settings.token.TOKEN_TYPE,
            access_token_expires=str(access_token_expires)
        )

    async def get_current_user(self, token: str, session: AsyncSession) -> User:
        payload = self._decode_access_token(token)
        email = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: email not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user = await user_service.get_user_by_email(email=email, session=session)
        except UserNotFoundExceptions as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex)
            )
        return user


auth_service = AuthService()
