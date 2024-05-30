from uuid import UUID
import enum
from litestar.contrib.sqlalchemy.base import UUIDAuditBase, UUIDBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from users.models import UserModel


class Command(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class ChatModel(UUIDBase):
    __tablename__ = "chats"
    name: Mapped[str]
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel", secondary="chatusers", lazy="selectin"
    )


class ChatUserModel(UUIDBase):
    __tablename__ = "chatusers"
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class MessageModel(UUIDAuditBase):
    __tablename__ = "messages"
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    author: Mapped["UserModel"] = relationship("UserModel", lazy="selectin")
    text: Mapped[str]


class ChatRepository(SQLAlchemyAsyncRepository[ChatModel]):
    model_type = ChatModel


class MessageRepository(SQLAlchemyAsyncRepository[MessageModel]):
    model_type = MessageModel


async def provide_chat_repository(db_session: AsyncSession) -> ChatRepository:
    return ChatRepository(session=db_session)


async def provide_message_repository(db_session: AsyncSession) -> MessageRepository:
    return MessageRepository(session=db_session)
