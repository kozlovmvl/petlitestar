from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


class UserModel(UUIDBase):
    __tablename__ = "users"
    email: Mapped[str]
    username: Mapped[str]


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
    model_type = UserModel


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)


