from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.db.models.user_model import UserRole


class GetMeResponse(BaseModel):
    nickname: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: str
    profile_image: Optional[str] = None
    role: Optional[UserRole] = None
    signed_at: datetime

    class Config:
        from_attributes = True
