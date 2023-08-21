from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.complaint import SelfComplaintException, AlreadyComplainedException


async def self_complaint_handler(request: Request, exc: SelfComplaintException):
    return JSONResponse(
        status_code=400,
        content={'message': 'You cannot complain about own content!'}
    )


async def already_complained_handler(request: Request, exc: AlreadyComplainedException):
    return JSONResponse(
        status_code=400,
        content={'message': 'You have already complained about this content!'}
    )
