from uuid import UUID
from litestar import Controller, WebSocket, get, post, put, delete, websocket
from litestar.channels import ChannelsPlugin
from litestar.di import Provide
from pydantic import TypeAdapter
from sqlalchemy import select
from chats.models import (
    ChatRepository,
    Command,
    MessageModel,
    MessageRepository,
    provide_chat_repository,
    provide_message_repository,
)

from chats.scheme import ChatSchema, MessageReadSchema, MessageWriteSchema, WSDataSchema


class ChatController(Controller):
    path = "chats"
    dependencies = {
        "chats_repo": Provide(provide_chat_repository),
    }

    @get("/")
    async def get_list(self, chats_repo: ChatRepository) -> list[ChatSchema]:
        objs = await chats_repo.list()
        type_adapter = TypeAdapter(list[ChatSchema])
        return type_adapter.validate_python(objs)


class MessageController(Controller):
    path = "chats/messages"
    dependencies = {
        "messages_repo": Provide(provide_message_repository),
    }

    @get("/")
    async def get_list(
        self, messages_repo: MessageRepository
    ) -> list[MessageReadSchema]:
        objs = await messages_repo.list(
            statement=select(MessageModel).order_by("created_at")
        )
        type_adapter = TypeAdapter(list[MessageReadSchema])
        return type_adapter.validate_python(objs)

    @post("/")
    async def create(
        self,
        data: MessageWriteSchema,
        messages_repo: MessageRepository,
        channels: ChannelsPlugin,
    ) -> None:
        obj = await messages_repo.add(
            MessageModel(**data.model_dump(exclude_unset=True))
        )
        await messages_repo.session.commit()
        obj = await messages_repo.get(obj.id)
        message = MessageReadSchema.model_validate(obj)
        await channels.wait_published(
            WSDataSchema(command=Command.CREATE, message=message).model_dump(),
            channels=[str(data.chat_id)],
        )

    @put("/{message_id:uuid}")
    async def update(
        self,
        message_id: UUID,
        data: MessageWriteSchema,
        messages_repo: MessageRepository,
        channels: ChannelsPlugin,
    ) -> None:
        raw_obj = MessageModel(**data.model_dump(exclude_unset=True))
        raw_obj.update({"id": message_id})
        await messages_repo.update(raw_obj)
        await messages_repo.session.commit()
        obj = await messages_repo.get(message_id)
        message = MessageReadSchema.model_validate(obj)
        await channels.wait_published(
            WSDataSchema(command=Command.UPDATE, message=message).model_dump(),
            channels=["chats"],
        )

    @delete("/{message_id:uuid}")
    async def delete(
        self,
        message_id: UUID,
        messages_repo: MessageRepository,
        channels: ChannelsPlugin,
    ) -> None:
        await messages_repo.delete(message_id)
        await messages_repo.session.commit()
        await channels.wait_published(
            WSDataSchema(
                command=Command.UPDATE, message=MessageReadSchema(id=message_id)
            ).model_dump(),
            channels=["chats"],
        )


@websocket(
    "/chats/{chat_id:uuid}",
    dependencies={"messages_repo": Provide(provide_message_repository)},
)
async def chat_handler(
    chat_id: UUID,
    messages_repo: MessageRepository,
    channels: ChannelsPlugin,
    socket: WebSocket,
) -> None:
    await socket.accept()
    async with channels.start_subscription([str(chat_id)]) as subscriber:
        async for message in subscriber.iter_events():
            await socket.send_text(message)
