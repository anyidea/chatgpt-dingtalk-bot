"""Main module."""
from fastapi import FastAPI, Body
from .gpt import AsyncChatbot

from .models import DingtalkAskMessage

app = FastAPI()


temperature = 0.5

# Initialize chatbot
chatbot = AsyncChatbot()


@app.post("/chat")
async def chat(message: DingtalkAskMessage):
    prompt = message.text.content.strip()
    nickname = message.senderNick
    if prompt.startswith("清空会话"):
        chatbot.reset()

    response = await chatbot.ask(prompt, temperature=temperature, user=nickname)
    reply = response["choices"][0]["text"].strip()
    return {"text": {"content": reply}, "msgtype": "text"}
