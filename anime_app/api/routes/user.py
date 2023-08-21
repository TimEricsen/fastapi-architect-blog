from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from anime_app.core.models import dto
from anime_app.core.services.user import user_register
from anime_app.api.dependencies.auth import AuthProvider, get_current_user
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.db import dao_provider


router = APIRouter(tags=['User'], prefix='/user')


@router.post('/token')
async def login(form_date: OAuth2PasswordRequestForm = Depends(),
                dao: HolderDao = Depends(dao_provider),
                auth: AuthProvider = Depends()) -> dto.Token:
    user = await auth.authenticate_user(form_date.username, form_date.password, dao.user)
    return auth.create_user_token(user)


@router.get('/me')
async def get_user_me(current_user: dto.MainUser = Depends(get_current_user)) -> dto.MainUser:
    return current_user


@router.post('/registration')
async def user_registration(user: dto.CreateUser,
                            dao: HolderDao = Depends(dao_provider),
                            auth: AuthProvider = Depends()) -> dto.MainUser:
    return await user_register(user, dao.user, auth)
