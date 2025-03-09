import datetime
import uuid
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import BaseModel
from sqlalchemy import select
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


class Payload(BaseModel):
    user_id: Optional[str] = None
    sub_id: Optional[str] = None
    jti: Optional[str] = None
    exp: int


def generate_access_token(user_id: uuid.UUID, sub_id: str) -> str:
    expire = datetime.datetime.now() + datetime.timedelta(hours=1)
    payload = {
        "user_id": str(user_id),
        "sub_id": sub_id,
        "exp": int(expire.timestamp()),
    }

    access_jwt = jwt.encode(payload, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return access_jwt


def generate_refresh_token() -> str:
    expire = datetime.datetime.now() + datetime.timedelta(days=7)
    payload = {
        "jti": str(uuid.uuid4()),
        "exp": int(expire.timestamp()),
    }

    refresh_jwt = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return refresh_jwt


def decode_access_token(token: str, verify_exp: bool) -> Payload:
    try:
        payload = jwt.decode(
            token,
            ACCESS_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": verify_exp},
        )

        print(payload)

        return Payload(**payload)
    except:
        raise HTTPException(status_code=401)


def decode_refresh_token(token: str) -> Payload:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])

        return Payload(**payload)
    except:
        raise HTTPException(status_code=401)


async def get_user(user_id: str, db: Session) -> User:
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalars().first()
    # user = db.query(User).filter(User.id == user_id).one_or_none() ## < V2.0

    if not user:
        raise HTTPException(status_code=401)

    return user


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(Provide["db_session"]),
) -> User:
    payload = decode_access_token(token=token, verify_exp=True)
    print(payload)
    user_id = payload.user_id

    user = await get_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=401)

    return user
