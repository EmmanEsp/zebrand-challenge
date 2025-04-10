from pydantic import BaseModel

from typing import Optional


class UserRequest(BaseModel):
    
    name: str
    role: str
    email: str
    password: str


class PatchUserRequest(BaseModel):
    
    name: Optional[str]
    role: Optional[str]
    email: Optional[str]
    password: Optional[str]
