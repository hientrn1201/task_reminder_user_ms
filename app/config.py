# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TASK_SERVICE_URL: str
    REMINDER_SERVICE_URL: str
    USER_SERVICE_URL: str
    FRONTEND_URL: str
    COMPOSITE_SERVICE_URL: str
    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
