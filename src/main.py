# main.py
from containers import Container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.users.controller.user_controller import router as users_router

app = FastAPI()
app.container = Container()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 허용할 오리진을 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)