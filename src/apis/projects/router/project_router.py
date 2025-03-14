from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from src.apis.projects.dto.request.create_project_request import CreateProjectRequest
from src.apis.projects.dto.response.get_projects_response import (
    GetProjectsResponse,
    GetProjectData,
)
from src.apis.projects.service.project_service import ProjectService
from src.common.jwt import get_current_user
from src.db.models.user_model import User, UserRole

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


@router.post("", dependencies=[Depends(HTTPBearer())])
@inject
async def create_project(
    body: CreateProjectRequest,
    project_service: ProjectService = Depends(Provide["project_service"]),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403)

    await project_service.create_project(body)
