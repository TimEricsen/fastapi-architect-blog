from typing import Union

from datetime import date
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None


class CreateUser(BaseUser):
    password: Union[str, None] = None
    repeat_password: Union[str, None] = None


class MainUser(BaseUser):
    id: Union[int, None] = None
    creation_date: Union[date, None] = None
    hashed_password: Union[str, None] = None

    class Config:
        orm_mode = True


class BLUser(BaseUser):
    id: Union[int, None] = None

    class Config:
        orm_mode = True
