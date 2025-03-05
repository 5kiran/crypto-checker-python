from dependency_injector import containers, providers

from src.apis.auth.service.auth_service import AuthService
from src.apis.users.repositories.user_repo import UserRepository
from src.apis.users.service.user_service import UserService
from src.db.database import get_db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=["src.apis.auth", "src.apis.users"],
        auto_wire=True,
    )

    db_session = providers.Resource(get_db)
    auth_service = providers.Factory(AuthService)
    user_repository = providers.Factory(UserRepository, db=db_session)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
