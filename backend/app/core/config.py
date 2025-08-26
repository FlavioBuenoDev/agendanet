# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore") # type: ignore
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings()