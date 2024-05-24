import enum
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from users.models import UserModel


class Command(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class MessageModel(UUIDAuditBase):
    __tablename__ = "messages"
    author_id: Mapped["UserModel"] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    author: Mapped["UserModel"] = relationship("UserModel", lazy="selectin")
    text: Mapped[str]


class MessageRepository(SQLAlchemyAsyncRepository[MessageModel]):
    model_type = MessageModel


async def provide_message_repository(db_session: AsyncSession) -> MessageRepository:
    return MessageRepository(session=db_session)
