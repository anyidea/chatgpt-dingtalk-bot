from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


class ConversationTypeEnum(str, Enum):
    single = "1"  # 单聊
    group = "2"  # 群聊


class MessageTypeEnum(str, Enum):
    text = "text"
    # markdown = "markdown"


class AskAtUsers(BaseModel):
    dingtalkId: str
    staffId: Optional[str]


class TextMessage(BaseModel):
    content: str


class MarkdownMessage(BaseModel):
    title: str
    text: str


class DingtalkAskMessage(BaseModel):
    conversationId: str  # 会话ID
    atUsers: list[AskAtUsers]  # 被@人的信息
    chatbotCorpId: Optional[str] = ""  # 加密的机器人所在的企业corpId
    chatbotUserId: str  # 加密的机器人ID
    msgId: str  # 加密的消息ID
    senderNick: str  # 发送者昵称
    isAdmin: Optional[bool]  # 是否为管理员,机器人发布上线后生效
    senderStaffId: Optional[str] = ""  # 发送者userid,该字段在机器人发布线上版本后，才会返回
    sessionWebhookExpiredTime: int  # 当前会话的Webhook地址过期时间
    createAt: int  # 消息的时间戳，单位ms
    senderCorpId: Optional[str] = ""  # 企业内部群有的发送者当前群的企业corpId
    conversationType: ConversationTypeEnum  # 1：单聊 2：群聊
    senderId: str  # 加密的发送者
    conversationTitle: Optional[str] = ""  # 群聊时才有的会话标题
    isInAtList: Optional[bool]  # 是否在@列表中
    sessionWebhook: HttpUrl  # 当前会话的Webhook地址
    text: TextMessage  # 文本消息
    msgtype: MessageTypeEnum  # 目前只支持text
