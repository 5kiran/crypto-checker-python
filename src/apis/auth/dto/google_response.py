from typing import Optional

from pydantic import BaseModel


class GoogleAuthResponse(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    nbf: int
    name: Optional[str]
    picture: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    iat: int
    exp: int
    jti: str
