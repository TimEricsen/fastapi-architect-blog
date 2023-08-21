from typing import Protocol


class LikeCreator(Protocol):
    async def like_post(self, post_id: int, username: str) -> str:
        raise NotImplementedError


class MyLikesGetter(Protocol):
    async def my_likes(self, username: str):
        raise NotImplementedError
