from anime_app.core.utils.exceptions.base import BaseAppException


class SelfAddToBLException(BaseAppException):
    pass


class UserAlreadyInBLException(BaseAppException):
    def __init__(self, user_id: int):
        self.user_id = user_id


class UserNotInBLException(BaseAppException):
    def __init__(self, user_id: int):
        self.user_id = user_id


class EmptyBLException(BaseAppException):
    pass


class UserInBLException(BaseAppException):
    pass
