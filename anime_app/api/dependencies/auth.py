from typing import Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError

from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.core.interfaces.dal.user import UserByUsernameGetter
from anime_app.core.utils.exceptions.user import IncorrectUsernameOrPasswordException, CredentialException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token', auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dto.MainUser:
    raise NotImplementedError


def get_current_user_or_pass(token: str = Depends(optional_oauth2_scheme)) -> dto.MainUser:
    raise NotImplementedError


class AuthProvider:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.algorythm = 'HS256'
        self.secret_key = 'SECRET'
        self.access_token_expire = timedelta(minutes=30)

    def password_comparison(self, password: str, confirm_password: str) -> bool:
        return password == confirm_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str,
                                dao: UserByUsernameGetter) -> dto.MainUser:
        user = await dao.get_by_username(username)
        if not user:
            raise IncorrectUsernameOrPasswordException
        if not self.verify_password(password, user.hashed_password):
            raise IncorrectUsernameOrPasswordException
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta) -> dto.Token:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorythm)
        return dto.Token(access_token=encoded_jwt, token_type='bearer')

    def create_user_token(self, user: dto.MainUser) -> dto.Token:
        return self.create_access_token(
            data={'sub': user.username}, expires_delta=self.access_token_expire
        )

    async def get_current_user(self, token: str = Depends(oauth2_scheme),
                               dao: HolderDao = Depends(dao_provider)) -> dto.MainUser:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorythm])
            username = payload.get('sub')
            if username is None:
                raise CredentialException
        except JWTError:
            raise CredentialException

        user = await dao.user.get_by_username(username)

        if not user:
            raise CredentialException
        return user

    async def get_current_user_or_pass(self, token: str = Depends(optional_oauth2_scheme),
                                       dao: HolderDao = Depends(dao_provider)) -> Union[dto.MainUser, None]:
        if not token:
            return None
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorythm])
            username = payload.get('sub')
            if username is None:
                raise CredentialException
        except JWTError:
            raise CredentialException

        user = await dao.user.get_by_username(username)

        if not user:
            raise CredentialException
        return user
