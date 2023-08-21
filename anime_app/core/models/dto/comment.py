from datetime import datetime
from pydantic import BaseModel
from typing import Union, List, Optional


class BaseComment(BaseModel):
    text: Union[str, None] = None


class CreateComment(BaseComment):
    pass


class EditComment(BaseComment):
    pass


class MainComment(BaseComment):
    author: Union[str, None] = None
    time_posted: Union[datetime, None] = None
    post_id: Union[int, None] = None
    likes: Union[int, None] = None

    class Config:
        orm_mode = True


class ParentComment(MainComment):
    answers: Optional[List[MainComment]] = None

    class Config:
        orm_mode = True
