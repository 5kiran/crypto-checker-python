from dependency_injector.wiring import inject

from ..repositories.interfaces.user_repo_interface import IUserRepository


class UserService:
    @inject
    def __init__(
        self,
        user_repository: IUserRepository,
    ):
        self.user_repository = user_repository

    async def get_user(self, token: str) -> str:
        # email = await self.user_repository.find_by_email(email=token)

        return token
