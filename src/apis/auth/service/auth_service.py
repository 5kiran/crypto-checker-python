from datetime import datetime

from dependency_injector.wiring import Provide
from fastapi import HTTPException
from fastapi.params import Depends
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from src.apis.auth.dto.response.auth_response import AuthResponse
from src.apis.auth.dto.response.google_response import GoogleAuthResponse
from src.apis.users.service.user_service import UserService
from src.common.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from src.config import get_setting
from src.db.models.user_model import User

settings = get_setting()


class AuthService:
    def __init__(
        self,
        user_service: UserService = Depends(Provide["user_service"]),
        db: Session = Depends(Provide["db_session"]),
    ):
        self.db = db
        self.user_service = user_service
        self.google_client_id = settings.google_client_id

    async def get_temp_token(self, google_sub) -> AuthResponse:
        user = await self.user_service.get_user_by_sub_id(google_sub)

        new_refresh_token = generate_refresh_token()
        new_access_token = generate_access_token(
            user_id=str(user.id), sub_id=user.sub_id
        )

        user.refresh_token = new_refresh_token
        user.updated_at = datetime.now()

        self.db.commit()
        return AuthResponse(
            access_token=new_access_token, refresh_token=new_refresh_token
        )

    async def auth_google(self, token: str) -> AuthResponse:
        try:
            _response = id_token.verify_oauth2_token(
                id_token=token,
                request=google_requests.Request(),
                audience=self.google_client_id,
            )
        except:
            raise HTTPException(status_code=500, detail="구글 API 에러")

        if not _response:
            raise HTTPException(status_code=403, detail="구글 유저 정보 조회 실패")

        google_response = GoogleAuthResponse(**_response)
        user = await self.user_service.get_user_by_sub_id(google_response.sub_id)
        refresh_token = generate_refresh_token()

        if not user:
            new_user = User(
                nickname="테스트",
                name=google_response.name,
                email=google_response.email,
                profile_image=google_response.profile_image,
                refresh_token=refresh_token,
                sub_id=google_response.sub_id,
            )

            user = await self.user_service.create_user(new_user)
        else:
            user.refresh_token = refresh_token
            user.updated_at = datetime.now()

        access_token = generate_access_token(user_id=str(user.id), sub_id=user.sub_id)

        self.db.commit()
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_jwt_token(
        self, access_token: str, refresh_token: str
    ) -> AuthResponse:
        decode_refresh_token(refresh_token)
        access_payload = decode_access_token(token=access_token, verify_exp=False)
        user_id = access_payload.user_id

        user = await self.user_service.get_user_by_refresh_token(refresh_token)

        if not user or str(user.id) != user_id:
            raise HTTPException(status_code=401)

        new_refresh_token = generate_refresh_token()
        new_access_token = generate_access_token(
            user_id=str(user.id), sub_id=user.sub_id
        )

        user.refresh_token = new_refresh_token
        user.updated_at = datetime.now()

        self.db.commit()
        return AuthResponse(
            access_token=new_access_token, refresh_token=new_refresh_token
        )
