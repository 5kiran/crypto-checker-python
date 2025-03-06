from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.apis.auth.dto.auth_response import AuthResponse
from src.apis.auth.service.auth_service import AuthService
from src.common.jwt import get_current_user
from src.db.models.user_model import User

router = APIRouter(prefix="/auth", tags=["auth"])


class GoogleAuthBody(BaseModel):
    token: str


@router.post("/google")
@inject
async def google_auth(
    body: GoogleAuthBody,
    auth_service: AuthService = Depends(Provide["auth_service"]),
) -> AuthResponse:
    auth_response = await auth_service.auth_google(body.token)
    return auth_response


@router.get("/access-token", dependencies=[Depends(HTTPBearer())])
@inject
async def get_access_token(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh-token")
@inject
async def refresh_jwt_token(
    access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    auth_service: AuthService = Depends(Provide["auth_service"]),
):
    if not refresh_token or not access_token:
        raise HTTPException(status_code=401)

    auth_response = await auth_service.refresh_jwt_token(
        access_token=access_token.credentials, refresh_token=refresh_token
    )

    return auth_response
