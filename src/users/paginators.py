from pydantic import TypeAdapter
from users.scheme import UserReadSchema
from utils import AbstractAsyncPaginator


class UserPaginator(AbstractAsyncPaginator):
    async def get_items(
        self, page_size: int, current_page: int
    ) -> list[UserReadSchema]:
        start = current_page * page_size
        stop = start + page_size
        r = await self.async_session.scalars(self.stmt.slice(start, stop))
        type_adapter = TypeAdapter(list[UserReadSchema])
        return type_adapter.validate_python(r)
