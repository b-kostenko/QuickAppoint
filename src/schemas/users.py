from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    uuid: str
    username: str
    email: str