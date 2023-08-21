from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.user import UserIDNotFoundException, IncorrectUsernameOrPasswordException, \
    CredentialException, PasswordMismatch, UsernameAlreadyExistsException, EmailAlreadyExistsException


async def user_id_not_found_handler(request: Request, exc: UserIDNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': f'User with id {exc.user_id} not found!'}
    )


async def credential_exception(request: Request, exc: CredentialException):
    return JSONResponse(
        status_code=401,
        content={'message': 'Could not validate credentials'},
        headers={'WWW-Authenticate': 'Bearer'}
    )


async def password_mismatch(request: Request, exc: PasswordMismatch):
    return JSONResponse(
        status_code=400,
        content={'message': 'Password mismatch!'}
    )


async def username_exists_handler(request: Request, exc: UsernameAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={'message': 'This username is already used!'}
    )


async def email_exists_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={'message': 'This email is already used!'}
    )


async def incorrect_username_or_password_handler(request: Request, exc: IncorrectUsernameOrPasswordException):
    return JSONResponse(
        status_code=400,
        content={'message': 'Incorrect username or password!'}
    )
