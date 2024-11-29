# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TASK_SERVICE_URL: str
    REMINDER_SERVICE_URL: str
    USER_SERVICE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
