from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.apis.auth.dto.request.google_auth_request import GoogleAuthRequest
from src.apis.auth.dto.response.auth_response import AuthResponse
from src.apis.auth.service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/temp-token", description="임시로 만든 함수")
@inject
async def temp_token(
    google_sub: str,
    auth_service: AuthService = Depends(Provide["auth_service"]),
) -> AuthResponse:
    auth_response = await auth_service.get_temp_token(google_sub)

    return auth_response


@router.post("/google")
@inject
async def google_auth(
    body: GoogleAuthRequest,
    auth_service: AuthService = Depends(Provide["auth_service"]),
) -> AuthResponse:
    auth_response = await auth_service.auth_google(body.token)
    return auth_response


@router.post("/refresh-token")
@inject
async def refresh_jwt_token(
    access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    auth_service: AuthService = Depends(Provide["auth_service"]),
) -> AuthResponse:
    if not refresh_token or not access_token:
        raise HTTPException(status_code=401)

    auth_response = await auth_service.refresh_jwt_token(
        access_token=access_token.credentials, refresh_token=refresh_token
    )

    return auth_response
