import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from src.db.models.mission_model import MissionType
from src.db.models.wallet_model import WalletType


class GetWalletMissionResponse(BaseModel):
    id: uuid.UUID
    type: MissionType
    title: str
    url: str
    start_at: datetime.datetime
    end_at: datetime.datetime
    draw_at: Optional[datetime.datetime] = None
    reward_date: Optional[datetime.date] = None

    class Config:
        from_attributes = True


class GetWalletJoinedMissionResponse(BaseModel):
    joined_at: datetime.datetime
    mission: GetWalletMissionResponse

    class Config:
        from_attributes = True


class GetWalletResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: WalletType
    address: str

    joined_missions: list[GetWalletJoinedMissionResponse]

    class Config:
        from_attributes = True
