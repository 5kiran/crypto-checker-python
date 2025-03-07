from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.db.models.user_model import UserRole


class ModifyUserResponse(BaseModel):
    nickname: str
    name: Optional[str]
    phone_number: Optional[str]
    email: str
    profile_image: Optional[str]
    role: Optional[UserRole]
    signed_at: datetime
