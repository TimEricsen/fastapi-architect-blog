from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.favourites import PostAlreadyInFavouritesException, PostNotInFavouritesException


async def post_in_favourites_handler(request: Request, exc: PostAlreadyInFavouritesException):
    return JSONResponse(
        status_code=400,
        content={'message': f'Post with id {exc.post_id} already in favourites!'}
    )


async def post_not_in_fav_handler(request: Request, exc: PostNotInFavouritesException):
    return JSONResponse(
        status_code=404,
        content={'message': f'Post with id {exc.post_id} not in favourites!'}
    )
