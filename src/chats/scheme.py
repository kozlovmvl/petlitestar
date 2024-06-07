from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from chats.models import Command
from users.scheme import UserChatSchema


class ChatSchema(BaseModel):
    id: UUID
    name: str
    count: int
    users: list["UserChatSchema"]

    model_config = {"from_attributes": True}


class MessageWriteSchema(BaseModel):
    id: Optional[UUID] = None
    chat_id: Optional[UUID] = None
    text: Optional[str] = None
    author_id: Optional[UUID] = None


class MessageReadSchema(BaseModel):
    id: UUID
    text: Optional[str] = None
    author: Optional["AuthorSchema"] = None

    model_config = {"from_attributes": True}


class AuthorSchema(BaseModel):
    id: UUID
    username: str

    model_config = {"from_attributes": True}


class WSDataSchema(BaseModel):
    command: Command
    message: Optional[MessageReadSchema] = None
