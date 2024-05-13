from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


class CityModel(UUIDBase):
    __tablename__ = "cities"
    name: Mapped[str]


class CityRepository(SQLAlchemyAsyncRepository[CityModel]):
    model_type = CityModel


async def provide_city_repository(db_session: AsyncSession) -> CityRepository:
    return CityRepository(session=db_session)
