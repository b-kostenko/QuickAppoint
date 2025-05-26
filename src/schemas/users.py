from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str