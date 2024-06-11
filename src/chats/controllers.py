from uuid import UUID
from litestar import Controller, WebSocket, get, post, put, delete, websocket
from litestar.channels import ChannelsPlugin
from litestar.di import Provide
from litestar.pagination import ClassicPagination
from sqlalchemy import desc, select, func
from chats.models import (
    ChatModel,
    ChatRepository,
    Command,
    MessageModel,
    MessageRepository,
    provide_chat_repository,
    provide_message_repository,
)

from chats.scheme import ChatSchema, MessageReadSchema, MessageWriteSchema, WSDataSchema
from chats.paginators import ChatPaginator, MessagePaginator


class ChatController(Controller):
    path = "chats"
    dependencies = {
        "chats_repo": Provide(provide_chat_repository),
    }

    @get("/")
    async def get_list(
        self, page_size: int, current_page: int, chats_repo: ChatRepository
    ) -> ClassicPagination[ChatSchema]:
        paginator = ChatPaginator(
            async_session=chats_repo.session,
            stmt=select(ChatModel, func.count(MessageModel.id))
            .join(MessageModel)
            .group_by(ChatModel.id),
            count_stmt=select(func.count(ChatModel.id)),
        )
        return await paginator(current_page=current_page, page_size=page_size)


class MessageController(Controller):
    path = "chats/messages"
    dependencies = {
        "messages_repo": Provide(provide_message_repository),
    }

    @get("/{chat_id:uuid}")
    async def get_list(
        self,
        chat_id: UUID,
        current_page: int,
        page_size: int,
        messages_repo: MessageRepository,
    ) -> ClassicPagination[MessageReadSchema]:
        paginator = MessagePaginator(
            async_session=messages_repo.session,
            stmt=select(MessageModel)
            .where(MessageModel.chat_id == chat_id)
            .order_by(desc("created_at")),
            count_stmt=select(func.count(MessageModel.id), MessageModel.chat_id)
            .where(MessageModel.chat_id == chat_id)
            .group_by(MessageModel.chat_id),
        )
        return await paginator(current_page=current_page, page_size=page_size)

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
        raw_obj = data.model_dump(exclude_unset=True)
        raw_obj.update({"id": message_id})
        await messages_repo.update(MessageModel(**raw_obj))
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
