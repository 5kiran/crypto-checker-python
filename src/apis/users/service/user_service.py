from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.orm import Session

from src.apis.users.dto.request.modify_user_request import ModifyUserRequest
from src.apis.users.repositories.interfaces.user_repo_interface import IUserRepository
from src.db.models.user_model import User


class UserService:
    @inject
    def __init__(
        self,
        user_repository: IUserRepository,
        db: Session = Depends(Provide["db_session"]),
    ):
        self.user_repository = user_repository
        self.db = db

    async def get_user_by_sub_id(self, sub_id: str) -> User:
        user = await self.user_repository.get_user_by_sub_id(sub_id)

        return user

    async def create_user(self, new_user: User) -> User:

        user = await self.user_repository.create_user(new_user)

        return user

    async def get_user_by_refresh_token(self, refresh_token: str) -> User:
        user = await self.user_repository.get_user_by_refresh_token(refresh_token)

        return user

    async def modify_user(self, body: ModifyUserRequest, user: User) -> User:
        for key, value in body:
            setattr(user, key, value)

        self.db.commit()
        return user
