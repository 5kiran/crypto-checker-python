from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.orm import Session

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
