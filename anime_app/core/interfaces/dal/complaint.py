from typing import Protocol

from anime_app.core.models import dto


class ComplaintCreator(Protocol):
    async def create_complaint(self, post_id: int, username: str, complaint: dto.CreateComplaint):
        raise NotImplementedError
