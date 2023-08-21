from typing import Protocol


class CommentLikeCreator(Protocol):
    async def like_comment(self, post_id: int, comment_id: int, username: str):
        raise NotImplementedError
