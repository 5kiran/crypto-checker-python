import uuid
from typing import Optional

from pydantic import BaseModel


class GetProjectData(BaseModel):
    id: uuid.UUID
    name: str
    image: str
    home_page: str
    git_hub: Optional[str] = None
    discord: Optional[str] = None
    twitter: Optional[str] = None
    twitter_handle: Optional[str] = None
    contract: Optional[str] = None
    test_contract: Optional[str] = None

    class Config:
        from_attributes = True


class GetProjectsResponse(BaseModel):
    projects: list[GetProjectData]
    total: int
    current_page: int
