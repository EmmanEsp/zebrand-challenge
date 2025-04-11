from pydantic import BaseModel, EmailStr, Field

from typing import Optional


class UserRequest(BaseModel):
    
    name: str
    role: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class PatchUserRequest(BaseModel):
    
    name: str = None
    role: str = None
    email: EmailStr = None
    password: str = None
