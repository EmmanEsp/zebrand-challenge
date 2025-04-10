from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse 

from app.domain.responses.api_response import APIResponse
from app.domain.enums import api_status


class UserException(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


async def user_exception_handler(request: Request, ex: UserException):
    api_response = APIResponse(
        service_status=api_status.FAIL,
        status_code=ex.status_code,
        data=ex.detail)
    return JSONResponse(content=api_response.model_dump(), status_code=ex.status_code)
