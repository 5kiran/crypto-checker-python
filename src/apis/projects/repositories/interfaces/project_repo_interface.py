from abc import ABCMeta, abstractmethod

from src.db.models.project_model import Project


class IProjectRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_projects(self, page: int, size: int) -> tuple[list[Project], int]:
        pass

    @abstractmethod
    async def create_project(self, project: Project) -> Project:
        pass
