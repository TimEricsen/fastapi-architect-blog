from typing import Protocol, Union, List

from anime_app.core.interfaces.dal.base import Committer
from anime_app.core.models import dto


class FromFavouriteBlackListDeleter(Committer, Protocol):
    async def remove_posts_from_favourites_if_added_to_black_list(self, user_id: int, post_author: str) -> None:
        raise NotImplementedError


class FavouriteAdder(Protocol):
    async def add_to_favourites(self, post_id: int, username: str) -> str:
        raise NotImplementedError


class FavouriteDeleter(Protocol):
    async def delete_from_favourites(self, post_id: int, username: str) -> str:
        raise NotImplementedError


class MyFavouritesGetter(Protocol):
    async def my_favourites(self, username: str) -> Union[List[dto.MainPost], str]:
        raise NotImplementedError
