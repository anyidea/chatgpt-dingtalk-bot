"""Main module."""
from fastapi import BackgroundTasks, FastAPI
from revChatGPT.V1 import AsyncChatbot
from .config import gpt_settings
from .dingtalk import DingtalkCorpAPI

from .schemas import ConversationTypeEnum, DingtalkAskMessage


app = FastAPI()

# Initialize chatbot
chatbot = AsyncChatbot(config=gpt_settings.dict(exclude_unset=True))
dingtalk_sdk = DingtalkCorpAPI()


async def reply(
    prompt: str,
    nickname: str,
    sender_userid: str,
    webhook_url: str,
    conversation_type: str,
):
    """发送群聊信息"""
    response = ""
    async for data in await chatbot.ask(
        prompt
    ):
        response = data["message"].strip()

    # 群聊时加上@
    if conversation_type == ConversationTypeEnum.group:
        response = f"@{sender_userid}\n\n{response}"

    payload = {"text": {"content": response}, "msgtype": "text"}
    if sender_userid:
        payload["at"] = {"atUserIds": [sender_userid]}

    await dingtalk_sdk.robot_webhook_send(webhook_url, json=payload)


@app.post("/chat")
async def chat(message: DingtalkAskMessage, background_tasks: BackgroundTasks):
    prompt = message.text.content.strip()
    nickname = message.senderNick
    sender_userid = message.senderStaffId
    webhook_url = message.sessionWebhook
    if prompt.startswith("清空会话"):
        chatbot.reset()

    if prompt == "":
        return

    background_tasks.add_task(
        reply,
        prompt,
        nickname,
        sender_userid,
        webhook_url,
        message.conversationType,
    )
    return "ok"
