from src.apis.users.repositories.interfaces.user_repo_interface import IUserRepository
from src.db.database import Session
from src.db.models.user_model import User


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    async def save(self, user: str):
        users = self.db.get()
        print(users)
        return "HI"

    async def find_by_email(self, email: str):
        users = self.db.query(User).all()

        for user in users:
            for wallet in user.wallets:
                print(wallet.name)
        return users
