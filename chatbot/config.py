from typing import Optional

from pydantic import BaseSettings


class ChatGPTSettings(BaseSettings):
    api_key: Optional[str]
    temperature: float = 0.5
    max_tokens: int = None
    proxy: Optional[str]
    model: Optional[str] = "gpt-3.5-turbo-0613"

    class Config:
        env_file = ".env"
        partial = True
        env_prefix = 'GPT_'


class DingtalkSettings(BaseSettings):
    app_key: str
    app_secret: str
    stream_enable: bool = True
    stream_size: int = 10

    class Config:
        env_file = ".env"
        env_prefix = 'DINGTALK_'


gpt_settings = ChatGPTSettings()
dingtalk_settings = DingtalkSettings()
