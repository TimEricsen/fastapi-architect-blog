from typing import Union
from pydantic import BaseModel


class MainLike(BaseModel):
    post_id: Union[int, None] = None
    username: Union[str, None] = None

    class Config:
        orm_mode = True
