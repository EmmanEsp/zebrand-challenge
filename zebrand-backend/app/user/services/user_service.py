from fastapi import Depends
from sqlalchemy.orm import Session

from app.infraestructure.database import get_db
from app.user.domain.models.user_model import UserModel


class UserService:
    
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self._db = db
        
    def get_user_by_email(self, email: str) -> UserModel:
        user = self._db.query(UserModel).filter(UserModel.email == email).first()
        return user
    
    def save_user(self, user: UserModel):
        self._db.add(user)
        self._db.commit()
