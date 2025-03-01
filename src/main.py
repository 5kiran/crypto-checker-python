from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.users.router.user_router import router as users_router
from src.containers import Container
from src.db.database import Base
from src.db.database import engine

app = FastAPI()
container = Container()
container.init_resources()
app.container = container

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
