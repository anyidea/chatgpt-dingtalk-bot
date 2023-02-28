from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Integer, UUID
from sqlalchemy.sql import func
import asyncio
import datetime
from typing import List
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

metadata = sqlalchemy.MetaData()

Conversation = sqlalchemy.Table(
    "conversation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, sqlite_autoincrement=True),
    sqlalchemy.Column("gpt_conversation", sqlalchemy.UUID),
    sqlalchemy.Column("dingtalk_conversation", sqlalchemy.UUID),
    sqlalchemy.Column("conversation_title", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("parent_conversation", sqlalchemy.UUID),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),
)
