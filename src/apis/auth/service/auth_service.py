import os

from dependency_injector.wiring import inject
from dotenv import load_dotenv
from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from pydantic import BaseModel

load_dotenv()


class GoogleAuthResponse(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    nbf: int | None
    name: str | None
    picture: str | None
    given_name: str | None
    family_name: str | None
    iat: int
    exp: int
    jti: str | None


class AuthService:
    def __init__(self):
        self.google_client_id = os.environ.get("GOOGLE_CLIENT_ID")

    async def verify_token(self, token: str) -> GoogleAuthResponse:
        try:
            response = id_token.verify_oauth2_token(
                token, google_requests.Request(), self.google_client_id
            )
        except:
            raise HTTPException(status_code=500, detail="Google Auth Error")

        if not response:
            raise HTTPException(status_code=403, detail="유저 정보를 찾을 수 없습니다.")

        # user = GoogleAuthResponse.model_validate(response)

        return response
