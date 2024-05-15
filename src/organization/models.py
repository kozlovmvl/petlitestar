from uuid import UUID
from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CountryModel(UUIDBase):
    __tablename__ = "countries"
    name: Mapped[str] = mapped_column(unique=True)


class CityModel(UUIDBase):
    __tablename__ = "cities"
    name: Mapped[str]
    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE")
    )
    country: Mapped["CountryModel"] = relationship("CountryModel", lazy="selectin")


class CountryRepository(SQLAlchemyAsyncRepository[CountryModel]):
    model_type = CountryModel


class CityRepository(SQLAlchemyAsyncRepository[CityModel]):
    model_type = CityModel


async def provide_country_repository(db_session: AsyncSession) -> CountryRepository:
    return CountryRepository(session=db_session)


async def provide_city_repository(db_session: AsyncSession) -> CityRepository:
    return CityRepository(session=db_session)
