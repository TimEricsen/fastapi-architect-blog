from typing import List
from datetime import datetime

from anime_app.core.models import dto
from anime_app.api.dependencies.auth import AuthProvider
from anime_app.infrastructure.db.models.user import User
from anime_app.core.interfaces.dal.user import UserExistenceChecker, UserFromBLGetter, UserRegisterAdder, UserByIDGetter
from anime_app.core.utils.exceptions.user import PasswordMismatch, UsernameAlreadyExistsException, \
    EmailAlreadyExistsException


async def user_register(user: dto.CreateUser,
                        dao: UserRegisterAdder,
                        auth: AuthProvider):
    if not auth.password_comparison(user.password, user.repeat_password):
        raise PasswordMismatch

    user_by_username = await dao.get_by_username(user.username)
    if user_by_username:
        raise UsernameAlreadyExistsException
    user_by_email = await dao.get_by_email(user.email)
    if user_by_email:
        raise EmailAlreadyExistsException
    hashed_password = auth.hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        creation_date=datetime.utcnow()
    )
    await dao.add_new_user(new_user)
    await dao.commit()
    await dao.refresh_new_user(new_user)
    return new_user.to_dto()


async def get_users_from_black_list(black_list, dao: UserFromBLGetter) -> List[dto.BLUser]:
    return await dao.get_users_from_bl(black_list)


async def check_user_existence(user_id: int, dao: UserExistenceChecker) -> None:
    return await dao.check_user_by_id(user_id)


async def get_user_by_id(user_id: int, dao: UserByIDGetter) -> dto.BLUser:
    return await dao.get_by_id(user_id)
