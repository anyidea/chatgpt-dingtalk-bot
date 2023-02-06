"""Main module."""
from fastapi import FastAPI, BackgroundTasks
from .gpt import AsyncChatbot

from .models import DingtalkAskMessage
import httpx

app = FastAPI()


temperature = 0.5

# Initialize chatbot
chatbot = AsyncChatbot()


async def reply_dingtalk(prompt: str, nickname: str, sender_userid: str, webhook_url: str):
    response = await chatbot.ask(prompt, temperature=temperature, user=nickname)
    reply = response["choices"][0]["text"].strip()
    reply = f"@{sender_userid}\n\n{reply}"
    payload = {"text": {"content": reply}, "msgtype": "text"}
    if sender_userid:
        payload["at"] = {"atUserIds": [sender_userid]}

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json=payload)


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

    background_tasks.add_task(reply_dingtalk, prompt, nickname, sender_userid, webhook_url)
