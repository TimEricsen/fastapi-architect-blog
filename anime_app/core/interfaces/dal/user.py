from typing import Protocol, List

from anime_app.core.interfaces.dal.base import Committer
from anime_app.core.models import dto


class UserExistenceChecker(Committer, Protocol):
    async def check_user_by_id(self, user_id: int) -> None:
        raise NotImplementedError


class UserFromBLGetter(Committer, Protocol):
    async def get_users_from_bl(self, black_list) -> List[dto.BLUser]:
        raise NotImplementedError


class UserRegisterAdder(Committer, Protocol):
    async def get_by_username(self, username: str) -> dto.MainUser:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> dto.MainUser:
        raise NotImplementedError

    async def add_new_user(self, new_user) -> None:
        raise NotImplementedError

    async def refresh_new_user(self, new_user) -> None:
        raise NotImplementedError


class UserByIDGetter(Protocol):
    async def get_by_id(self, user_id) -> dto.BLUser:
        raise NotImplementedError


class UserByUsernameGetter(Protocol):
    async def get_by_username(self, username: str) -> dto.MainUser:
        raise NotImplementedError
