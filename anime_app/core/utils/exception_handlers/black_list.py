from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.black_list import SelfAddToBLException, EmptyBLException, UserInBLException, \
    UserAlreadyInBLException, UserNotInBLException


async def self_add_to_bl_handler(request: Request, exc: SelfAddToBLException):
    return JSONResponse(
        status_code=400,
        content={'message': 'You cannot list yourself in black list operations'}
    )


async def user_already_in_bl_handler(request: Request, exc: UserAlreadyInBLException):
    return JSONResponse(
        status_code=400,
        content={'message': f'User with id {exc.user_id} already in your bl!'}
    )


async def user_not_in_bl_handler(request: Request, exc: UserNotInBLException):
    return JSONResponse(
        status_code=404,
        content={'message': f'User with id {exc.user_id} not in your bl!'}
    )


async def empty_bl_handler(request: Request, exc: EmptyBLException):
    return JSONResponse(
        status_code=404,
        content={'message': 'Your black list is empty!'}
    )


async def user_in_bl_handler(request: Request, exc: UserInBLException):
    return JSONResponse(
        status_code=403,
        content={'message': 'You cannot perform this action because you are blacklisted by the user.'}
    )
