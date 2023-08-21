from typing import Union

from pydantic import BaseModel


class CommentLikeMain(BaseModel):
    comment_id: Union[int, None] = None
    user: Union[str, None] = None

    class Config:
        orm_mode = True
