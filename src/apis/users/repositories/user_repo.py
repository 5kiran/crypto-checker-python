from .interfaces.user_repo_interface import IUserRepository
from db.models.user_model import User

class UserRepository(IUserRepository): 
    def save(self,
             user: User):
        return user
    
    def find_by_email(self,
                      email: str):
        user = User(id='tet',name='te',email=email,password='tt')
    
        return user