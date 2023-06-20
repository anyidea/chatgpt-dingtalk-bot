from typing import Optional

from pydantic import BaseSettings


class ChatGPTSettings(BaseSettings):
    api_key: str
    temperature: Optional[float] = 0.5
    max_tokens: Optional[int] = None
    proxy: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo-0613"

    class Config:
        env_file = ".env"
        partial = True
        env_prefix = 'GPT_'


class DingtalkSettings(BaseSettings):
    app_key: str
    app_secret: str
    stream_enable: Optional[bool] = True
    stream_size: Optional[int] = 10

    class Config:
        env_file = ".env"
        env_prefix = 'DINGTALK_'


gpt_settings = ChatGPTSettings()
dingtalk_settings = DingtalkSettings()
