from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.like import LikesNotFoundException


async def like_not_found_handler(request: Request, exc: LikesNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': 'You have not liked any post or comment yet!'}
    )
