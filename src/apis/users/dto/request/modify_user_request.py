from typing import Optional

from pydantic import BaseModel


class ModifyUserRequest(BaseModel):
    nickname: str
    phone_number: Optional[str] = None
