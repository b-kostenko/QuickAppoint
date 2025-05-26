from typing import List

from fastapi import APIRouter

from src.schemas.users import UserDTO

router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/create")
async def create_user(user_data: UserDTO):
    pass

@router.get("/")
async def get_users() -> List[dict]:
    pass

@router.get("/{id}")
async def get_user_by_id(id: int) -> UserDTO:
    pass

@router.put("/{id}")
async def update_user(id: int) -> UserDTO:
    pass

@router.delete("/{id}")
async def delete_user(id: int) -> None:
    pass