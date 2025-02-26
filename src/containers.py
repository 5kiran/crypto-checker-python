from dependency_injector import containers, providers
from apis.users.repositories.user_repo import UserRepository
from apis.users.service.user_service import UserService
from apis.users.service.google_auth_service import GoogleAuthService

    
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    wiring_config = containers.WiringConfiguration(packages=["apis"],auto_wire=True)
    
    google_auth_service = providers.Factory(GoogleAuthService)
    user_repository = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService,user_repository=user_repository,google_auth_service=google_auth_service)