from typing import cast, Generic, TypeVar
from litestar.pagination import ClassicPagination
from sqlalchemy.ext.asyncio import AsyncSession

DataType = TypeVar("DataType")


class AbstractAsyncPaginator(Generic[DataType]):
    def __init__(self, async_session: AsyncSession, stmt, count_stmt):
        self.async_session = async_session
        self.stmt = stmt
        self.count_stmt = count_stmt

    async def get_items(self, page_size: int, current_page: int) -> list[DataType]:
        raise NotImplementedError

    async def get_total(self, page_size: int) -> int:
        return round(
            cast("int", await self.async_session.scalar(self.count_stmt)) / page_size
        )

    async def __call__(
        self, page_size: int, current_page: int
    ) -> ClassicPagination[DataType]:
        return ClassicPagination[DataType](
            items=await self.get_items(page_size=page_size, current_page=current_page),
            page_size=page_size,
            current_page=current_page,
            total_pages=await self.get_total(page_size),
        )
