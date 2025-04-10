from datetime import datetime

from fastapi import Depends, status
from argon2 import PasswordHasher

from app.user.services.user_service import UserService
from app.user.domain.requests.user_request import UserRequest, PatchUserRequest
from app.user.domain.models.user_model import UserModel
from app.user.domain.exceptions.user_exception import UserException


class UserUseCase:
    
    def __init__(self, user_service: UserService = Depends()) -> None:
        self.user_service = user_service
    
    def hash_password(self, password: str) -> str:
        hasher = PasswordHasher()
        return hasher.hash(password)

    def create_user(self, user: UserRequest):
        exists = self.user_service.get_user_by_email(user.email)
        if exists is not None:
            raise UserException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"email": "Email already in use."}
            )
        new_user = UserModel(
            name=user.name,
            role=user.role,
            email=user.email,
            password=self.hash_password(user.password)
        )
        self.user_service.save_user(new_user)
    
    def update_user(self, email: str, values: PatchUserRequest):
        user: UserModel = self.user_service.get_user_by_email(email)
        if user is None:
            raise UserException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"email": "User not found."}
            )
        
        update_data = values.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        self.user_service.save_user(user)

    def delete_user(self, email: str):
        user: UserModel = self.user_service.get_user_by_email(email)
        if user is None:
            raise UserException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"email": "User not found."}
            )
        user.deleted_at = datetime.now()
        self.user_service.save_user(user)
