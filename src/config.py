from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    python_env: str
    database_url: str
    google_client_id: str
    google_client_secret: str
    access_secret_key: str
    refresh_secret_key: str


@lru_cache
def get_setting():
    return Settings()
