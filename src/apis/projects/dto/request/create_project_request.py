from typing import Optional

from pydantic import BaseModel


class CreateProjectRequest(BaseModel):
    name: str
    image: str
    home_page: str
    git_hub: str
    discord: Optional[str] = None
    twitter: Optional[str] = None
    twitter_handle: Optional[str] = None
    contract: Optional[str] = None
    test_contract: bool
