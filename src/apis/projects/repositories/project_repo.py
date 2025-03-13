from dependency_injector.wiring import Provide
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.apis.projects.repositories.interfaces.project_repo_interface import (
    IProjectRepository,
)
from src.db.models.project_model import Project


class ProjectRepository(IProjectRepository):
    def __init__(self, db: Session = Depends(Provide["db_session"])):
        self.db = db

    async def get_projects(self, page: int, size: int) -> tuple[list[Project], int]:
        from sqlalchemy import select

        stmt = select(Project).offset((page - 1) * size).limit(size)
        projects = self.db.execute(stmt).scalars().all()

        total_count = self.db.execute(
            select(func.count()).select_from(Project)
        ).scalar()

        return list(projects), total_count
