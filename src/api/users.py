from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status
from fastapi.responses import JSONResponse
from src.api.dependencies import async_session_dep
from src.schemas.users import UserSchema, UserResponse, UserUpdateSchema
from src.services.user_service import user_service
from src.utils.exceptions import UserAlreadyExistsException

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_input: UserSchema, session: async_session_dep) -> UserResponse:
    try:
        user = await user_service.create_user(user_input=user_input, session=session)
        return user
    except UserAlreadyExistsException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ex)
        )


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(session: async_session_dep) -> List[UserResponse]:
    users = await user_service.get_users(session=session)
    return users


@router.get("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(email: str, session: async_session_dep) -> UserResponse:
    user = await user_service.get_user_by_email(email=email, session=session)
    return user


@router.put("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_input: UserUpdateSchema, email: str, session: async_session_dep) -> UserResponse:
    user = await user_service.update_user(user_input=user_input, email=email, session=session)
    return user


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str, session: async_session_dep) -> None:
    await user_service.delete_user(email=email, session=session)
