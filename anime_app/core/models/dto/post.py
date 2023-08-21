from datetime import datetime
from pydantic import BaseModel
from typing import Union, List, Optional

from anime_app.core.models import dto


class BasePost(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass


class MainPost(BasePost):
    id: Union[int, None] = None
    author: Union[str, None] = None
    publication_date: Union[datetime, None] = None
    likes: Union[int, None] = None

    class Config:
        orm_mode = True


class MainRetrievePost(BasePost):
    id: Union[int, None] = None
    author: Union[str, None] = None
    publication_date: Union[datetime, None] = None
    likes: Union[List[dto.MainLike], None] = None
    comments: Optional[List[dto.ParentComment]] = None

    class Config:
        orm_mode = True
