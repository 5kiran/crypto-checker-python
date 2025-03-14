from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.orm import Session

from src.apis.projects.dto.request.create_project_request import CreateProjectRequest
from src.apis.projects.repositories.interfaces.project_repo_interface import (
    IProjectRepository,
)
from src.db.models.project_model import Project


class ProjectService:
    @inject
    def __init__(
        self,
        project_repository: IProjectRepository,
        db: Session = Depends(Provide["db_session"]),
    ):
        self.db = db
        self.project_repository = project_repository

    async def get_projects(
        self, page: int, size: int
    ) -> tuple[list[Project], int, int]:
        projects, total = await self.project_repository.get_projects(
            page=page, size=size
        )

        return projects, total, page

    async def create_project(self, body: CreateProjectRequest) -> Project:
        _project = Project(
            name=body.name,
            image=body.image,
            home_page=body.home_page,
            git_hub=body.git_hub,
            discord=body.discord,
            twitter=body.twitter,
            twitter_handle=body.twitter_handle,
            contract=body.contract,
            test_contract=body.test_contract,
        )

        project = await self.project_repository.create_project(_project)

        self.db.commit()
        return project
