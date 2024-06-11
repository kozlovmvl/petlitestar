from pydantic import TypeAdapter
from organization.scheme import CityReadSchema, CountryReadSchema
from utils import AbstractAsyncPaginator


class CountryPaginator(AbstractAsyncPaginator):
    async def get_items(
        self, page_size: int, current_page: int
    ) -> list[CountryReadSchema]:
        start = page_size * current_page
        stop = start + page_size
        r = await self.async_session.scalars(self.stmt.slice(start, stop))
        type_adapter = TypeAdapter(list[CountryReadSchema])
        return type_adapter.validate_python(r)


class CityPaginator(AbstractAsyncPaginator):
    async def get_items(
        self, page_size: int, current_page: int
    ) -> list[CityReadSchema]:
        start = page_size * current_page
        stop = start + page_size
        r = await self.async_session.scalars(self.stmt.slice(start, stop))
        type_adapter = TypeAdapter(list[CityReadSchema])
        return type_adapter.validate_python(r)
