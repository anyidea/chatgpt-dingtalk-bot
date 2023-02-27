"""Main module."""
from typing import Any, Dict

from fastapi import BackgroundTasks, FastAPI

from .chatgpt import AsyncChatbotPool
from .constants import BUSSY_MESSAGE
from .dingtalk import DingtalkCorpAPI
from .schemas import ConversationTypeEnum, DingtalkAskMessage
from .utils import get_conversation_id, init_chatbots

app = FastAPI()

# Initialize chatbot
chatbots = init_chatbots()
pool = AsyncChatbotPool(chatbots)

dingtalk = DingtalkCorpAPI()


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
):
    """获取gpt回答"""
    response = ""
    chatbot = None
    try:
        chatbot = await pool.get_object()
        async for data in chatbot.ask(prompt):
            response = data["message"].strip()
    except Exception as e:
        if BUSSY_MESSAGE in str(e):
            response = "在发送另一条消息之前，请等待任何其他响应完成，或者等待一分钟。"
        else:
            response = str(e)
    finally:
        if chatbot:
            pool.release_object(chatbot)

    await callback_bot(webhook_url, response, conversation_type, sender_userid)


@app.post("/chat")
async def chat(message: DingtalkAskMessage, background_tasks: BackgroundTasks):
    prompt = message.text.content.strip()
    nickname = message.senderNick
    conversation_id = get_conversation_id(message.conversationId)
    conversation_type = message.conversationType
    sender_userid = message.senderStaffId
    webhook_url = message.sessionWebhook
    if prompt == "":
        return

    if prompt.startswith("清空会话"):
        for chatbot in chatbots:
            await chatbot.clear_conversations()
        await callback_bot(webhook_url, "会话已清空", conversation_type, sender_userid)
        return
    elif prompt.startswith("删除会话"):
        for chatbot in chatbots:
            await chatbot.delete_conversation(conversation_id)
        await callback_bot(webhook_url, "会话已删除", conversation_type, sender_userid)
        return
    elif prompt.startswith("重置会话"):
        for chatbot in chatbots:
            chatbot.reset_chat()
        await callback_bot(webhook_url, "会话已重置", conversation_type, sender_userid)
        return

    background_tasks.add_task(
        ask_and_reply,
        prompt,
        nickname,
        sender_userid,
        webhook_url,
        message.conversationType,
        conversation_id,
    )
    return "ok"
