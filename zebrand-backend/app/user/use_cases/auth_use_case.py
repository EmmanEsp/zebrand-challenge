from fastapi import Depends, status
from argon2 import PasswordHasher
from jose import jwt

from app.domain.settings.security_settings import get_security_setting
from app.user.services.user_service import UserService
from app.user.domain.exceptions.user_exception import UserException
from app.user.domain.requests.auth_request import AuthSigninRequest
from app.user.domain.responses.auth_response import AuthSigninResponse


class AuthUseCase:
    
    def __init__(self, user_service: UserService = Depends()) -> None:
        self._user_service = user_service
    
    def sign_in(self, request: AuthSigninRequest):
        user = self._user_service.get_user_by_email(request.email)
        hasher = PasswordHasher()

        if user is None or not hasher.verify(user.password, request.password):
            raise UserException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"auth": "Credentials do not match."}
            )
        
        settings = get_security_setting()
        payload = {
            "sub": user.email,
            "role": user.role
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        response = AuthSigninResponse(token=token)
        return response
    
    def guest(self):
        settings = get_security_setting()
        payload = {
            "sub": "guest@zebrand.com",
            "role": "guest"
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        response = AuthSigninResponse(token=token)
        return response
