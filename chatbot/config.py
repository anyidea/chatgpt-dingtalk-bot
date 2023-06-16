from typing import Optional

from pydantic import BaseSettings


class ChatGPTSettings(BaseSettings):
    accounts: Optional[str]
    access_tokens: Optional[str]
    temperature: Optional[float]
    disable_history: Optional[bool] = False
    proxy: Optional[str]
    model: Optional[str]
    paid: bool = False
    plugin_ids: Optional[str]
    base_url: Optional[str]
    PUID: Optional[str]

    class Config:
        env_file = ".env"
        partial = True
        env_prefix = 'GPT_'


class DingtalkSettings(BaseSettings):
    app_key: str = ""
    app_secret: str = ""

    class Config:
        env_file = ".env"
        env_prefix = 'DINGTALK_'


gpt_settings = ChatGPTSettings()
dingtalk_settings = DingtalkSettings()
