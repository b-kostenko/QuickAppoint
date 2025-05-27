from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies import async_session_dep
from src.schemas.token import TokenSchema
from src.schemas.users import UserLogin, UserResponse, UserSchema
from src.services.auth_service import auth_service
from src.services.user_service import user_service
from src.utils.exceptions import UserAlreadyExistsException, UserNotFoundExceptions

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK, description="Login")
async def login(user_credentials: UserLogin, session: async_session_dep) -> TokenSchema:
    try:
        user = await user_service.retrieve_user_info_by_email(email=user_credentials.email, session=session)
    except UserNotFoundExceptions as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex)
        )

    if not user or not user_service.verify_password(
            plain_password=user_credentials.password,
            hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_service.login_for_access_token(user=user)



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, description="Registration")
async def register(user_input: UserSchema, session: async_session_dep) -> UserResponse:
    try:
        user = await user_service.create_user(user_input=user_input, session=session)
        return user
    except UserAlreadyExistsException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ex)
        )