
class BaseUserException(Exception):

    def __init__(self,message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundExceptions(BaseUserException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' not found"
        )

class UserAlreadyExistsException(BaseUserException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists"
        )
