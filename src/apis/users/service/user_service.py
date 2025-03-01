from dependency_injector.wiring import inject

from .google_auth_service import GoogleAuthService
from ..repositories.interfaces.user_repo_interface import IUserRepository


class UserService:
    @inject
    def __init__(
        self,
        user_repository: IUserRepository,
        google_auth_service: GoogleAuthService,
    ):
        self.user_repository = user_repository
        self.google_auth_service = google_auth_service

    async def google_auth(self, token: str) -> str:
        _user = await self.google_auth_service.verify_token(token)

        user = self.user_repository.save()
        return user

    async def get_email(self, token: str) -> str:
        email = await self.user_repository.find_by_email(email=token)

        return email
