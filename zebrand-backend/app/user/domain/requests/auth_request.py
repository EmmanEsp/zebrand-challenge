from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class AuthSigninRequest(BaseModel):

    email: EmailStr
    password: Annotated[str, Field(max_length=100, min_length=8)] = None
