from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from organization.models import CityModel


class UserModel(UUIDBase):
    __tablename__ = "users"
    email: Mapped[str]
    username: Mapped[str]
    addresses: Mapped[list["AddressModel"]] = relationship(
        "AddressModel", lazy="selectin"
    )


class AddressModel(UUIDBase):
    __tablename__ = "addresses"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    city_id: Mapped[UUID] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    city: Mapped["CityModel"] = relationship("CityModel", lazy="selectin")


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
    model_type = UserModel


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)
