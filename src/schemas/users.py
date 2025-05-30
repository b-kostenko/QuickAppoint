from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdateSchema(BaseModel):
    username: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    uuid: str
    username: str
    email: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str