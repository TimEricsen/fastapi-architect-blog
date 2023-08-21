from typing import Protocol, List

from anime_app.core.models import dto
from anime_app.core.interfaces.dal.base import Committer


class PostCreator(Committer, Protocol):
    async def add_new_post(self, new_post) -> None:
        raise NotImplementedError

    async def refresh_new_post(self, new_post) -> None:
        raise NotImplementedError


class AllPostsGetter(Protocol):
    async def get_all_posts(self) -> List[dto.MainPost]:
        raise NotImplementedError


class PostByIDGetter(Protocol):
    async def get_post_with_comments_by_id(self, post_id: int) -> dto.MainRetrievePost:
        raise NotImplementedError


class PostByIDReturner(Protocol):
    async def return_post_by_id(self, post, comments) -> dto.MainRetrievePost:
        raise NotImplementedError


class PostsByQuerySearchGetter(Protocol):
    async def get_post_by_query_search(self, search: str) -> List[dto.MainPost]:
        raise NotImplementedError


class MyPostsGetter(Protocol):
    async def get_my_posts(self, username: str) -> List[dto.MainPost]:
        raise NotImplementedError


class PostUpdater(Protocol):
    async def update_post(self, post: dto.UpdatePost, post_id: int, username: str) -> str:
        raise NotImplementedError


class PostDeleter(Protocol):
    async def delete_post(self, post_id: int, username: str) -> str:
        raise NotImplementedError


class PostByUserGetter(Protocol):
    async def user_posts(self, author: str) -> List[dto.MainPost]:
        raise NotImplementedError


class SimplePostGetter(Protocol):
    async def get_post_by_id(self, post_id) -> dto.MainPost:
        raise NotImplementedError


class PostExistenceChecker(Protocol):
    async def check_post_existence(self, post_id: int) -> None:
        raise NotImplementedError
