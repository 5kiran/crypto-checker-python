from src.containers import Container
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.apis.auth.service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


class GoogleAuthBody(BaseModel):
    token: str


@router.post("/google")
@inject
async def google_auth(
    body: GoogleAuthBody,
    auth_service: AuthService = Depends(Provide["auth_service"]),
):
    user = await auth_service.verify_token(body.token)
    return user
