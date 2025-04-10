from fastapi import APIRouter

from app.user.api.v1.user_controller import user_v1_router
from app.user.api.v1.auth_controller import auth_v1_router


user_router = APIRouter()

user_router.include_router(
    user_v1_router,
    prefix="/api/v1/user",
    tags=["User"]
)

user_router.include_router(
    auth_v1_router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)
