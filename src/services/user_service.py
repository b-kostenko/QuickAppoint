from src.schemas.users import UserDTO


class UserService:

    def __init__(self):
        pass

    async def create_user(self, user_input: UserDTO):
        user_input.model_dump()