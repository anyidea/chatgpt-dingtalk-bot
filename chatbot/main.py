"""Main module."""
from fastapi import BackgroundTasks, FastAPI

from .config import settings
from .dingtalk import DingtalkCorpAPI
from .gpt import AsyncChatbot
from .schemas import ConversationTypeEnum, DingtalkAskMessage

app = FastAPI()


temperature = 0.5

# Initialize chatbot
chatbot = AsyncChatbot()
dingtalk_sdk = DingtalkCorpAPI()


async def reply_group(prompt: str, nickname: str, sender_userid: str, webhook_url: str):
    """发送群聊信息"""
    response = await chatbot.ask(
        prompt, temperature=settings.gpt_temperature, user=nickname
    )
    reply = response["choices"][0]["text"].strip()
    reply = f"@{sender_userid}\n\n{reply}"
    payload = {"text": {"content": reply}, "msgtype": "text"}
    if sender_userid:
        payload["at"] = {"atUserIds": [sender_userid]}

    await dingtalk_sdk.robot_webhook_send(webhook_url, json=payload)


async def reply_single(prompt: str, nickname: str, sender_userid: str, robot_code: str):
    """发送单聊信息"""
    response = await chatbot.ask(
        prompt, temperature=settings.gpt_temperature, user=nickname
    )
    reply = response["choices"][0]["text"].strip()
    reply = f"@{sender_userid}\n\n{reply}"
    params = {"content": reply}
    await dingtalk_sdk.robot_batch_send(
        robot_code, [sender_userid], "sampleText", params
    )


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

    if message.conversationType == ConversationTypeEnum.group:
        background_tasks.add_task(
            reply_group, prompt, nickname, sender_userid, webhook_url
        )
    else:
        background_tasks.add_task(
            reply_single, prompt, nickname, sender_userid, webhook_url
        )

    return "ok"
