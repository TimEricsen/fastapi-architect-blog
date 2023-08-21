from anime_app.core.utils.exceptions.base import BaseAppException


class UserIDNotFoundException(BaseAppException):
    def __init__(self, user_id: int):
        self.user_id = user_id


class IncorrectUsernameOrPasswordException(BaseAppException):
    pass


class CredentialException(BaseAppException):
    pass


class PasswordMismatch(BaseAppException):
    pass


class UsernameAlreadyExistsException(BaseAppException):
    pass


class EmailAlreadyExistsException(BaseAppException):
    pass
