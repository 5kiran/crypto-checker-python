import datetime
from typing import Optional

from dependency_injector.wiring import Provide
from fastapi.params import Depends
from sqlalchemy import select

from src.apis.users.repositories.interfaces.user_repo_interface import IUserRepository
from src.db.database import Session
from src.db.models.user_model import User


class UserRepository(IUserRepository):
    def __init__(self, db: Session = Depends(Provide["db_session"])):
        self.db = db

    async def create_user(self, user: User) -> User:
        self.db.add(user)

        return user

    async def get_user_by_sub_id(self, sub_id: str) -> Optional[User]:
        stmt = select(User).where(User.sub_id == sub_id)
        user = self.db.execute(stmt).scalars().first()
        # user = self.db.query(User).filter(User.sub_id == sub_id).one_or_none() ## < 2.0

        return user

    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        stmt = select(User).where(User.refresh_token == refresh_token)
        user = self.db.execute(stmt).scalars().first()
        # user = (
        #     self.db.query(User)
        #     .filter(User.refresh_token == refresh_token)
        #     .one_or_none()
        # )

        return user
