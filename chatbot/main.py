"""Main module."""
from fastapi import FastAPI, Body
from .gpt import AsyncChatbot

from .models import DingtalkAskMessage
import httpx

app = FastAPI()


temperature = 0.5

# Initialize chatbot
chatbot = AsyncChatbot()


@app.post("/chat")
async def chat(message: DingtalkAskMessage):
    prompt = message.text.content.strip()
    nickname = message.senderNick
    sender_userid = message.senderStaffId
    webhook_url = message.sessionWebhook
    if prompt.startswith("清空会话"):
        chatbot.reset()

    response = await chatbot.ask(prompt, temperature=temperature, user=nickname)
    reply = response["choices"][0]["text"].strip()
    payload = {"text": {"content": reply}, "msgtype": "text"}
    if sender_userid:
        payload["at"] = {"atUserIds": [sender_userid]}

    async with httpx.AsyncClient() as client:
        r = await client.post(webhook_url, json=payload)
        assert r.status_code == 200, "钉钉回调失败!"

    return payload
