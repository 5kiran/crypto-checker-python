from .interfaces.user_repo_interface import IUserRepository
from db.models.user_model import User
from sqlalchemy.orm import Session, lazyload

class UserRepository(IUserRepository):
    db: Session
    def save(self,
             user: User):
        return user
    
    def find_by_email(self,
                      email: str):
        user = User(id='tet',name='te',email=email,password='tt')
    
        return user