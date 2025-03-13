from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.apis.projects.dto.response.get_projects_response import (
    GetProjectsResponse,
    GetProjectData,
)
from src.apis.projects.service.project_service import ProjectService

router = APIRouter(prefix="/project", tags=["project"])


@router.get("")
@inject
async def get_projects(
    page: Optional[int] = 1,
    size: Optional[int] = 9,
    project_service: ProjectService = Depends(Provide["project_service"]),
) -> GetProjectsResponse:
    _projects, total, current_page = await project_service.get_projects(page, size)

    projects = [GetProjectData.model_validate(project) for project in _projects]

    return GetProjectsResponse(
        total=total, current_page=current_page, projects=projects
    )
