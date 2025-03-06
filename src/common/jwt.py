import uuid
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from sqlalchemy.orm import Session

from src.config import get_setting
from src.db.models.user_model import User

settings = get_setting()

ACCESS_SECRET_KEY = settings.access_secret_key
REFRESH_SECRET_KEY = settings.refresh_secret_key
ALGORITHM = "HS256"


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="/auth/google",  # 토큰 교환을 처리할 엔드포인트
)


def generate_access_token(user_id: str, sub_id: str) -> str:
    payload = {
        "user_id": user_id,
        "sub_id": sub_id,
    }

    access_jwt = jwt.encode(payload, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return access_jwt


def generate_refresh_token() -> str:
    payload = {
        "jti": str(uuid.uuid4()),
    }

    refresh_jwt = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return refresh_jwt


def decode_access_token(token: str, verify_exp: bool):
    try:
        payload = jwt.decode(
            token,
            ACCESS_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": verify_exp},
        )
        return payload
    except:
        raise HTTPException(status_code=401)


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except:
        raise HTTPException(status_code=401)


async def get_user(user_id: str, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="GET_USER")

    return user


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(Provide["db_session"]),
) -> User:
    payload = decode_access_token(token, True)
    user_id = payload["user_id"]

    user = await get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=401, detail="CURRENT_USER")

    return user
