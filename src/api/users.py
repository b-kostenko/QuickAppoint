from typing import List

from fastapi import APIRouter
from starlette import status

from src.api.dependencies import async_session_dep, current_user_dep
from src.schemas.users import UserResponse, UserUpdateSchema
from src.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK, description="List Users")
async def get_users(session: async_session_dep, _: current_user_dep) -> List[UserResponse]:
    users = await user_service.get_users(session=session)
    return users


@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK, description="Retrieve User")
async def profile(session: async_session_dep, current_user: current_user_dep) -> UserResponse:
    user = await user_service.get_user_by_email(email=current_user.email, session=session)
    return user


@router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK, description="Update User")
async def update_user(user_input: UserUpdateSchema, session: async_session_dep, current_user: current_user_dep) -> UserResponse:
    user = await user_service.update_user(user=current_user, user_input=user_input, session=session)
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, description="Delete User")
async def delete_user(session: async_session_dep, current_user: current_user_dep) -> None:
    await user_service.delete_user(user=current_user, session=session)
