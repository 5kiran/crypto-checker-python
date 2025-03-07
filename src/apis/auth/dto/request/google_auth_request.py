from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    token: str
