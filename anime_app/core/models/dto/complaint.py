import enum

from typing import Union
from pydantic import BaseModel


class ComplaintEnum(enum.Enum):
    first = 'Discriminatory speech or slander'
    second = 'Spam'
    third = 'Advertising of illegal content'


class BaseComplaint(BaseModel):
    reason: Union[ComplaintEnum, None] = None


class CreateComplaint(BaseComplaint):
    pass


class MainComplaint(BaseComplaint):
    id: Union[int, None] = None
    post_id: Union[int, None] = None
    user: Union[str, None] = None

    class Config:
        orm_mode = True
