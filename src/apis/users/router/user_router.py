from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.apis.users.dto.request.modify_user_request import ModifyUserRequest
from src.apis.users.dto.response.get_me_response import GetMeResponse

from src.apis.users.service.user_service import UserService
from src.common.jwt import get_current_user
from src.db.models.user_model import User

router = APIRouter(prefix="/user", tags=["user"])


@router.put("", dependencies=[Depends(HTTPBearer())])
@inject
async def update_user(
    body: ModifyUserRequest,
    user_service: UserService = Depends(Provide["user_service"]),
    current_user: User = Depends(get_current_user),
) -> GetMeResponse:
    user = await user_service.modify_user(body=body, user=current_user)

    return GetMeResponse.model_validate(user)


@router.get("/me", dependencies=[Depends(HTTPBearer())])
async def get_me(
    current_user: User = Depends(get_current_user),
) -> GetMeResponse:
    return GetMeResponse.model_validate(current_user)
