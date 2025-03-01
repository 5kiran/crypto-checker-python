from src.containers import Container
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.apis.users.service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


class GoogleAuthBody(BaseModel):
    token: str


@router.post("/auth/google")
@inject
async def google_auth(
    body: GoogleAuthBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = await user_service.google_auth(body.token)
    return user


@router.get("/email")
@inject
async def getEmail(
    email: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    print(user_service)
    user = await user_service.get_email(email)
    return user
