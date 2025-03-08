from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.apis.auth.router.auth_rotuer import router as auth_router
from src.apis.users.router.user_router import router as user_router
from src.containers import Container

container = Container()

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
