from fastapi import APIRouter, status, Depends

from app.domain.responses.api_response import APIResponse
from app.domain.enums import api_status
from app.user.use_cases.auth_use_case import AuthUseCase
from app.user.domain.requests.auth_request import AuthSigninRequest
from app.user.domain.responses.auth_response import AuthSigninResponse


auth_v1_router = APIRouter()


@auth_v1_router.post(
    "/sign-in",
    response_model=APIResponse[AuthSigninResponse],
    status_code=status.HTTP_200_OK
)
async def sign_in(request: AuthSigninRequest, use_case: AuthUseCase = Depends()):
    response = use_case.sign_in(request)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=response)


@auth_v1_router.post(
    "/guest",
    response_model=APIResponse[AuthSigninResponse],
    status_code=status.HTTP_200_OK
)
async def guest(use_case: AuthUseCase = Depends()):
    response = use_case.guest()
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=response)
