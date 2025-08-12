# app/core/config.py
from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

settings = Settings()