from anime_app.core.utils.exceptions.base import BaseAppException


class SelfComplaintException(BaseAppException):
    pass


class AlreadyComplainedException(BaseAppException):
    pass
