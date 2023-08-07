import uuid
import os
from revChatGPT.V3 import Chatbot

from .config import gpt_settings


def get_conversation_id(convo_id: str):
    """
    将钉钉会话id转成uuid
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, convo_id))


def get_chatbot_id(chatbot) -> str:
    return chatbot.config.get("email") or chatbot.config.get("access_token")


def init_chatbot():
    """
    初始化
    """
    config = gpt_settings

    if config.api_url is not None:
        os.environ["API_URL"] = config.api_url

    kwargs = {
        "api_key": config.api_key,
        "system_prompt": config.base_prompt,
        "proxy": config.proxy,
        "temperature": config.temperature,
        "reply_count": config.reply_count,
        "engine": config.model,
        "truncate_limit": config.truncate_limit,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    bot = Chatbot(**kwargs)
    return bot


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        # The actual exception depends on the specific database so we catch all exceptions.
        # This is similar to the official
        # documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
        except Exception:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True
