import asyncio
import datetime
from typing import List

import sqlalchemy
from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Column,
    ForeignKey,
    Integer,
    String,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.sql import func

from .database import Base

metadata = sqlalchemy.MetaData()

Conversation = sqlalchemy.Table(
    "conversation",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, sqlite_autoincrement=True
    ),
    sqlalchemy.Column("gpt_conversation", sqlalchemy.UUID),
    sqlalchemy.Column("dingtalk_conversation", sqlalchemy.UUID),
    sqlalchemy.Column("conversation_title", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("parent_conversation", sqlalchemy.UUID),
    sqlalchemy.Column(
        "created_at", sqlalchemy.DateTime, nullable=False, server_default=func.now()
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)
