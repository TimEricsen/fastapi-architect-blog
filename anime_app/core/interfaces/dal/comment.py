from typing import Protocol, List

from anime_app.core.models import dto


class CommentsForPostGetter(Protocol):
    async def get_pk_comments(self, pk: int) -> dto.ParentComment:
        raise NotImplementedError


class CommentAdder(Protocol):
    async def add_comment(self, post_id: int, comment: dto.CreateComment,
                          answer_to: int, username: str) -> dto.MainComment:
        raise NotImplementedError


class CommentEditor(Protocol):
    async def update_comment(self, post_id: int, comment_id: int, editable_comment: dto.EditComment,
                             username: str) -> str:
        raise NotImplementedError


class CommentDeleter(Protocol):
    async def delete_comment(self, post_id: int, comment_id: int, username: str, post_author: str) -> str:
        raise NotImplementedError


class MyCommentGetter(Protocol):
    async def my_comments(self, username: str) -> List[dto.MainComment]:
        raise NotImplementedError
