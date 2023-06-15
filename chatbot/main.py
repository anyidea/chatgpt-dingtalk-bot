"""Main module."""
from typing import Any, Dict

from fastapi import BackgroundTasks, FastAPI
from sqlalchemy import delete, insert, select, update

from .chatgpt import AsyncChatbotPool
from .constants import BUSSY_MESSAGE, WELCOME_MESSAGE
from .database import conversation, database
from .dingtalk import DingtalkCorpAPI
from .schemas import ConversationTypeEnum, DingtalkAskMessage
from .utils import get_conversation_id, init_chatbot, get_chatbot_id

# Initial app
app = FastAPI()
# Initialize chatbot
chatbot = init_chatbot()

dingtalk = DingtalkCorpAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def callback_bot(
    webhook_url: str, response: str, conversation_type: str, sender_userid: str = None
):
    """回调d"""
    title = response[:12]
    payload: Dict[str, Any] = {"msgtype": "text"}
    # 群聊时加上@
    if conversation_type == ConversationTypeEnum.group and sender_userid:
        response = f"@{sender_userid}\n\n{response}"
        payload["at"] = {"atUserIds": [sender_userid]}

    payload["text"] = {"title": f" {title}", "content": response}
    await dingtalk.robot_webhook_send(webhook_url, json=payload)


async def ask_and_reply(
    prompt: str,
    nickname: str,
    sender_userid: str,
    webhook_url: str,
    conversation_type: str,
    conversation_id: str,
    conversation_title: str,
):
    """获取gpt回答"""
    response = await chatbot.ask_async(
        prompt, convo_id=conversation_id, role=sender_userid
    )

    await callback_bot(webhook_url, response, conversation_type, sender_userid)


@app.post("/chat")
async def chat(message: DingtalkAskMessage, background_tasks: BackgroundTasks):
    prompt = message.text.content.strip()
    nickname = message.senderNick
    conversation_id = get_conversation_id(message.conversationId)
    conversation_type = message.conversationType
    sender_userid = message.senderStaffId
    webhook_url = message.sessionWebhook
    conversation_title = message.conversationTitle

    if prompt.lower() in ("", "帮助", "help"):
        await callback_bot(
            webhook_url, WELCOME_MESSAGE, conversation_type, sender_userid
        )
        return
    elif prompt.startswith("重置"):
        chatbot.reset(convo_id=conversation_id)
        await callback_bot(webhook_url, "会话已重置", conversation_type, sender_userid)
        return

    background_tasks.add_task(
        ask_and_reply,
        prompt,
        nickname,
        sender_userid,
        webhook_url,
        conversation_type,
        conversation_id,
        conversation_title,
    )
    return
