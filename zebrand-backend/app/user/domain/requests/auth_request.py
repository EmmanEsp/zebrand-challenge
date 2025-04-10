from pydantic import BaseModel


class AuthSigninRequest(BaseModel):

    email: str
    password: str
