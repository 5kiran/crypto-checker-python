from typing import Optional

from pydantic import BaseModel, Field


class GoogleAuthResponse(BaseModel):
    iss: str
    azp: str
    aud: str
    sub_id: str = Field(alias="sub")
    email: str
    email_verified: bool
    nbf: int
    name: Optional[str]
    profile_image: Optional[str] = Field(alias="picture")
    given_name: Optional[str]
    family_name: Optional[str]
    iat: int
    exp: int
    jti: str
