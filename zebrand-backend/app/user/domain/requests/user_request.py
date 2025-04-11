from pydantic import BaseModel, EmailStr, Field

from typing import Annotated


class UserRequest(BaseModel):
    
    name: Annotated[str, Field(max_length=60, min_length=3)]
    role: Annotated[str, Field(max_length=10, min_length=2)]
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class PatchUserRequest(BaseModel):
    
    name: Annotated[str, Field(max_length=60, min_length=3)] = None
    role: Annotated[str, Field(max_length=10, min_length=2)] = None
    email: EmailStr = None
    password: Annotated[str, Field(max_length=100, min_length=8)] = None
