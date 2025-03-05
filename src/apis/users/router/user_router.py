from src.containers import Container
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.apis.users.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


class GoogleAuthBody(BaseModel):
    token: str


@router.get("/email")
@inject
async def getEmail(
    email: str,
    user_service: UserService = Depends(Provide["user_service"]),
):
    print(user_service)
    user = await user_service.get_email(email)
    return user
