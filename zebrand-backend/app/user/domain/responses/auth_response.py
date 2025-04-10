from pydantic import BaseModel


class AuthSigninResponse(BaseModel):

    token: str
