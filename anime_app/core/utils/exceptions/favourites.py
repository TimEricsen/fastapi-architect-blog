from anime_app.core.utils.exceptions.base import BaseAppException


class PostAlreadyInFavouritesException(BaseAppException):
    def __init__(self, post_id: int):
        self.post_id = post_id


class PostNotInFavouritesException(BaseAppException):
    def __init__(self, post_id: int):
        self.post_id = post_id
