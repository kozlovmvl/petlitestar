from pydantic import TypeAdapter

from chats.scheme import ChatSchema, MessageReadSchema
from utils import AbstractAsyncPaginator


class ChatPaginator(AbstractAsyncPaginator):
    async def get_items(self, page_size: int, current_page: int) -> list[ChatSchema]:
        start = current_page * page_size
        stop = start + page_size
        r = await self.async_session.execute(self.stmt.slice(start, stop))
        objs = []
        for item in r:
            item[0].count = item[1]
            objs.append(ChatSchema.model_validate(item[0]))
        return objs


class MessagePaginator(AbstractAsyncPaginator):
    async def get_items(
        self, page_size: int, current_page: int
    ) -> list[MessageReadSchema]:
        start = current_page * page_size
        stop = start + page_size
        r = await self.async_session.scalars(self.stmt.slice(start, stop))
        type_adapter = TypeAdapter(list[MessageReadSchema])
        return type_adapter.validate_python(r)
