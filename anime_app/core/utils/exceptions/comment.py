from anime_app.core.utils.exceptions.base import BaseAppException


class CommentNotFoundOrNotCreatorException(BaseAppException):
    pass


class CommentsNotFoundException(BaseAppException):
    pass
