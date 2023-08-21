from typing import Protocol

from anime_app.core.models import dto


class CommentComplaintAdder(Protocol):
    async def add_comment_complaint(self, post_id: int, comment_id: int, username: str,
                                    reason: dto.CreateCommentComplaint) -> str:
        raise NotImplementedError
