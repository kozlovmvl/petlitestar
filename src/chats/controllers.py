from litestar import WebSocket
from litestar.handlers import WebsocketListener
from litestar.di import Provide
from pydantic import TypeAdapter
from sqlalchemy import select
from chats.models import (
    Command,
    MessageModel,
    MessageRepository,
    provide_message_repository,
)

from chats.scheme import MessageReadSchema, RequestSchema, ResponseSchema


class ChatController(WebsocketListener):
    path = "chats"
    dependencies = {"messages_repo": Provide(provide_message_repository)}

    async def on_accept(self, socket: WebSocket, messages_repo: MessageRepository):
        objs = await messages_repo.list(
            statement=select(MessageModel).order_by("created_at")
        )
        type_adapter = TypeAdapter(list[MessageReadSchema])
        await socket.send_json(
            [obj.model_dump() for obj in type_adapter.validate_python(objs)]
        )

    async def on_disconnect(self, socket: WebSocket) -> None:
        print("Connection closed")

    async def on_receive(
        self, data: str, messages_repo: MessageRepository
    ) -> ResponseSchema:
        request = RequestSchema.model_validate_json(data)
        match request.command:
            case Command.CREATE:
                return await self._create_message(request, messages_repo)
            case Command.UPDATE:
                return await self._update_message(request, messages_repo)
            case Command.DELETE:
                return await self._delete_message(request, messages_repo)

    async def _create_message(
        self, data: RequestSchema, messages_repo: MessageRepository
    ) -> ResponseSchema:
        obj = await messages_repo.add(
            MessageModel(**data.message.model_dump(exclude_unset=True))
        )
        await messages_repo.session.commit()
        return ResponseSchema(
            command=Command.CREATE, message=MessageReadSchema.model_validate(obj)
        )

    async def _update_message(
        self, data: RequestSchema, messages_repo: MessageRepository
    ) -> ResponseSchema:
        raw_obj = MessageModel(**data.message.model_dump(exclude_unset=True))
        await messages_repo.update(raw_obj)
        await messages_repo.session.commit()
        obj = await messages_repo.get(data.message.id)
        return ResponseSchema(
            command=Command.UPDATE, message=MessageReadSchema.model_validate(obj)
        )

    async def _delete_message(
        self, data: RequestSchema, messages_repo: MessageRepository
    ) -> ResponseSchema:
        await messages_repo.delete(data.message.id)
        await messages_repo.session.commit()
        return ResponseSchema(
            command=Command.DELETE, message=MessageReadSchema(id=data.message.id)
        )
