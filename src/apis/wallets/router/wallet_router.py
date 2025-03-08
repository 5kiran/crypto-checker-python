from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.apis.wallets.dto.request.create_wallet_request import CreateWalletRequest
from src.apis.wallets.dto.response.create_wallet_response import CreateWalletResponse
from src.apis.wallets.dto.response.get_wallet_response import GetWalletResponse
from src.apis.wallets.service.wallet_service import WalletService
from src.common.jwt import get_current_user
from src.db.models.user_model import User

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post("", dependencies=[Depends(HTTPBearer())])
@inject
async def create_wallet(
    body: CreateWalletRequest,
    wallet_service: WalletService = Depends(Provide["wallet_service"]),
    current_user: User = Depends(get_current_user),
) -> CreateWalletResponse:
    wallet = await wallet_service.create_wallet(body=body, user=current_user)

    return CreateWalletResponse.model_validate(wallet)


@router.get("", dependencies=[Depends(HTTPBearer())])
@inject
async def get_wallets(
    wallet_service: WalletService = Depends(Provide["wallet_service"]),
    current_user: User = Depends(get_current_user),
) -> list[GetWalletResponse]:
    wallets = await wallet_service.get_wallets(user=current_user)

    return [GetWalletResponse.model_validate(wallet) for wallet in wallets]
