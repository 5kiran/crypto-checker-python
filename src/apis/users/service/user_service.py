from dependency_injector.wiring import inject

from src.apis.auth.dto.google_response import GoogleAuthResponse
from src.apis.users.repositories.interfaces.user_repo_interface import IUserRepository
from src.db.models.user_model import User


class UserService:
    @inject
    def __init__(
        self,
        user_repository: IUserRepository,
    ):
        self.user_repository = user_repository

    async def get_user_by_sub_id(self, sub_id: str) -> User:
        user = await self.user_repository.get_user_by_sub_id(sub_id)

        return user

    async def create_user(
        self, google_response: GoogleAuthResponse, refresh_token: str
    ) -> User:
        new_user = User(
            nickname="테스트",
            name=google_response["name"],
            email=google_response["email"],
            profile_image=google_response["picture"],
            refresh_token=refresh_token,
            sub_id=google_response["sub"],
        )

        user = await self.user_repository.create_user(new_user)

        return user

    async def update_user(self, user: User) -> User:
        user = await self.user_repository.update_user(user)

        return user

    async def get_user_by_refresh_token(self, refresh_token: str) -> User:
        user = await self.user_repository.get_user_by_refresh_token(refresh_token)

        return user
