from pydantic import BaseSettings
from typing import Optional


class ChatGPTSettings(BaseSettings):
    email: Optional[str]
    password: Optional[str]
    access_token: Optional[str]
    conversation_id: Optional[str]
    parent_id: Optional[str]
    proxy: Optional[str]
    paid: bool = False

    class Config:
        env_file = ".env"
        partial = True
        env_prefix = 'GPT_'


class DingtalkSettings(BaseSettings):
    app_key: str
    app_secret: str

    class Config:
        env_file = ".env"
        env_prefix = 'DINGTALK_'


gpt_settings = ChatGPTSettings()
dingtalk_settings = DingtalkSettings()
