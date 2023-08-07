from typing import Optional

from pydantic import BaseSettings


class ChatGPTSettings(BaseSettings):
    api_key: str
    api_url: Optional[str] = None
    temperature: Optional[float] = 0.5
    max_tokens: Optional[int] = None
    base_prompt: Optional[str] = None
    reply_count: Optional[int] = None
    truncate_limit: Optional[int] = None
    proxy: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
        partial = True
        env_prefix = 'GPT_'


class DingtalkSettings(BaseSettings):
    app_key: str
    app_secret: str
    stream_enable: Optional[bool] = False
    stream_size: Optional[int] = 15

    class Config:
        env_file = ".env"
        env_prefix = 'DINGTALK_'


gpt_settings = ChatGPTSettings()
dingtalk_settings = DingtalkSettings()
