from anime_app.core.utils.exceptions.base import BaseAppException


class PostIDNotFoundException(BaseAppException):
    def __init__(self, post_id: int):
        self.post_id = post_id


class NotPositivePostIDException(BaseAppException):
    pass


class PostOrCommentNotFoundException(BaseAppException):
    pass


class NotPostOwnerException(BaseAppException):
    pass


class EmptyPostListException(BaseAppException):
    pass


class PostNotFoundOrNotCreatorException(BaseAppException):
    pass
