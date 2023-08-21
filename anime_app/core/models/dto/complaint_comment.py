from typing import Union
from pydantic import BaseModel

from anime_app.core.models.dto.complaint import ComplaintEnum


class BaseCommentComplaint(BaseModel):
    reason: Union[ComplaintEnum, None] = None


class CreateCommentComplaint(BaseCommentComplaint):
    pass


class MainCommentComplaint(BaseCommentComplaint):
    id: Union[int, None] = None
    comment_id: Union[int, None] = None
    user: Union[str, None] = None

    class Config:
        orm_mode = True
