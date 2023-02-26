from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    email: Optional[str]
    password: Optional[str]
    access_token: Optional[str]
    conversation_id: Optional[str]
    parent_id: Optional[str]
    proxy: Optional[str]
    paid: bool = False
    dingtalk_app_key: str = ""
    dingtalk_app_secret: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
