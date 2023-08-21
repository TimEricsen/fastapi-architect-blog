from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.base import InaccessibleCharactersException


async def inaccessible_characters_handler(request: Request, exc: InaccessibleCharactersException):
    return JSONResponse(
        status_code=400,
        content={'message': 'You possibly using inaccessible characters! Please, try again!'}
    )
