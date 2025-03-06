from dependency_injector.wiring import Provide
from fastapi import HTTPException
from fastapi.params import Depends
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from src.apis.auth.dto.auth_response import AuthResponse
from src.apis.users.service.user_service import UserService
from src.common.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from src.config import get_setting

settings = get_setting()


class AuthService:
    def __init__(self, user_service: UserService = Depends(Provide["user_service"])):
        self.user_service = user_service
        self.google_client_id = settings.google_client_id

    async def auth_google(self, token: str) -> AuthResponse:
        try:
            response = id_token.verify_oauth2_token(
                token, google_requests.Request(), self.google_client_id
            )
        except:
            raise HTTPException(status_code=500, detail="구글 API 에러")

        if not response:
            raise HTTPException(status_code=403, detail="구글 유저 정보 조회 실패")

        user = await self.user_service.get_user_by_sub_id(response["sub"])
        print(user)
        refresh_token = generate_refresh_token()

        if not user:

            print("GI")
            user = await self.user_service.create_user(response, refresh_token)
        else:
            user.refresh_token = refresh_token
            await self.user_service.update_user(user)

        access_token = generate_access_token(str(user.id), user.sub_id)

        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_jwt_token(self, access_token: str, refresh_token: str):
        decode_refresh_token(refresh_token)
        access_payload = decode_access_token(access_token, False)
        user_id = access_payload.get("user_id")

        user = await self.user_service.get_user_by_refresh_token(refresh_token)

        if not user or str(user.id) != user_id:
            raise HTTPException(status_code=401)

        new_refresh_token = generate_refresh_token()
        new_access_token = generate_access_token(str(user.id), user.sub_id)

        user.refresh_token = new_refresh_token
        await self.user_service.update_user(user)

        return AuthResponse(
            access_token=new_access_token, refresh_token=new_refresh_token
        )
