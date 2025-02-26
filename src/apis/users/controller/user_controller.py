from containers import Container
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import Provide
from ..service.user_service import UserService
from ..service.google_auth_service import GoogleAuthService

router = APIRouter(prefix="/users",tags=["users"])

class GoogleAuthBody(BaseModel):
    token: str
    
@router.post('/auth/google')
@inject
async def google_auth(body : GoogleAuthBody, 
                      user_service : UserService = Depends(Provide[Container.user_service]),
                      ):
    
    user = await user_service.google_auth(body.token)
    return user
    
