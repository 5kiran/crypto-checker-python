from typing import Optional

from pydantic import BaseModel


class ModifyUserRequest(BaseModel):
    nickname: Optional[str] = None
    phone_number: Optional[str] = None
