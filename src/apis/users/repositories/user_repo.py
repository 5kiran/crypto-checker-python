import datetime

from dependency_injector.wiring import Provide
from fastapi.params import Depends

from src.apis.users.repositories.interfaces.user_repo_interface import IUserRepository
from src.db.database import Session
from src.db.models.user_model import User


class UserRepository(IUserRepository):
    def __init__(self, db: Session = Depends(Provide["db_session"])):
        self.db = db

    async def create_user(self, user: User) -> User:
        user = self.db.add(user)

        return user

    async def update_user(self, user: User) -> User:
        user.updated_at = datetime.datetime.now()
        user = self.db.query(User)

        return user

    async def get_user_by_sub_id(self, sub_id: str) -> User | None:
        user = self.db.query(User).filter(User.sub_id == sub_id).one_or_none()

        return user

    async def get_user_by_refresh_token(self, refresh_token: str) -> User | None:
        user = (
            self.db.query(User)
            .filter(User.refresh_token == refresh_token)
            .one_or_none()
        )

        return user
