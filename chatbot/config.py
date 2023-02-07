from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    gpt_temperature: float
    gpt_engine: str
    dingtalk_app_key: str
    dingtalk_app_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
