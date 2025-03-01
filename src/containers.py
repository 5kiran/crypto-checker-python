from dependency_injector import containers, providers

from src.db.database import get_db

from src.apis.users.repositories.user_repo import UserRepository
from src.apis.users.service.google_auth_service import GoogleAuthService
from src.apis.users.service.user_service import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(packages=["apis"], auto_wire=True)

    db_session = providers.Resource(get_db)
    google_auth_service = providers.Factory(GoogleAuthService)
    user_repository = providers.Factory(UserRepository, db=db_session)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        google_auth_service=google_auth_service,
    )
