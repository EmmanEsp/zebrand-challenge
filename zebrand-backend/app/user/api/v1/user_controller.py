from fastapi import APIRouter, status, Depends

from app.domain.responses.api_response import APIResponse
from app.domain.enums import api_status
from app.user.use_cases.user_use_case import UserUseCase
from app.user.api.v1 import user_documentation
from app.user.domain.requests.user_request import UserRequest, PatchUserRequest


user_v1_router = APIRouter()


@user_v1_router.post(
    "",
    response_model=APIResponse[None],
    responses=user_documentation.create_user_responses,
    status_code=status.HTTP_201_CREATED
)
async def create_user(request: UserRequest, use_case: UserUseCase = Depends()):
    use_case.create_user(request)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_201_CREATED,
        data=None)


@user_v1_router.patch(
    "/{email}",
    response_model=APIResponse[None],
    responses=user_documentation.update_user_responses,
    status_code=status.HTTP_200_OK
)
async def update_user(email: str, request: PatchUserRequest, use_case: UserUseCase = Depends()):
    use_case.update_user(email, request)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=None)


@user_v1_router.delete(
    "/{email}",
    response_model=APIResponse[None],
    responses=user_documentation.update_user_responses,
    status_code=status.HTTP_200_OK
)
async def delete_user(email: str, use_case: UserUseCase = Depends()):
    use_case.delete_user(email)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=None)
