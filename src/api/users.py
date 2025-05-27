from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies import async_session_dep
from src.schemas.users import UserSchema, UserResponse
from src.services.user_service import user_service
from src.utils.exceptions import UserAlreadyExistsException

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserSchema, session: async_session_dep) -> UserResponse:
    try:
        user = await user_service.create_user(user_input=user_data, session=session)
        return user
    except UserAlreadyExistsException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ex)
        )


@router.get("/")
async def get_users() -> List[dict]:
    pass


@router.get("/{id}")
async def get_user_by_id(id: int) -> UserSchema:
    pass


@router.put("/{id}")
async def update_user(id: int) -> UserSchema:
    pass


@router.delete("/{id}")
async def delete_user(id: int) -> None:
    pass
