from dependency_injector import containers, providers

from src.apis.auth.service.auth_service import AuthService
from src.apis.projects.repositories.project_repo import ProjectRepository
from src.apis.projects.service.project_service import ProjectService
from src.apis.users.repositories.user_repo import UserRepository
from src.apis.users.service.user_service import UserService
from src.apis.wallets.repositories.wallet_repo import WalletRepository
from src.apis.wallets.service.wallet_service import WalletService
from src.db.database import get_db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.apis.auth",
            "src.apis.users",
            "src.apis.wallets",
            "src.apis.projects",
        ],
        auto_wire=True,
    )

    db_session = providers.Resource(get_db)

    user_repository = providers.Factory(UserRepository, db=db_session)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        db=db_session,
    )

    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        db=db_session,
    )

    wallet_repository = providers.Factory(WalletRepository, db=db_session)
    wallet_service = providers.Factory(
        WalletService,
        wallet_repository=wallet_repository,
        db=db_session,
    )

    project_repository = providers.Factory(ProjectRepository, db=db_session)
    project_service = providers.Factory(
        ProjectService, project_repository=project_repository, db=db_session
    )
