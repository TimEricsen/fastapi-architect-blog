from typing import Union, List
from pydantic import BaseModel

from anime_app.core.models import dto


class PostCommentLikes(BaseModel):
    posts: Union[List[dto.MainPost], None] = None
    comments: Union[List[dto.MainComment], None] = None
