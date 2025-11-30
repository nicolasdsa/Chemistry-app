from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Chemistry API"
    database_url: str = "sqlite:///./app.db"
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
