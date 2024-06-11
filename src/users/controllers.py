from uuid import UUID
from litestar import Controller, get, post, delete, put
from litestar.di import Provide
from litestar.pagination import ClassicPagination
from sqlalchemy import asc, func, select

from users.models import (
    AddressModel,
    UserModel,
    UserRepository,
    provide_user_repository,
)
from users.paginators import UserPaginator
from users.scheme import UserReadSchema, UserCreateSchema, UserUpdateSchema


class UserController(Controller):
    path = "users"
    dependencies = {"users_repo": Provide(provide_user_repository)}

    @get("/")
    async def get_list(
        self, page_size: int, current_page: int, users_repo: UserRepository
    ) -> ClassicPagination[UserReadSchema]:
        paginator = UserPaginator(
            async_session=users_repo.session,
            stmt=select(UserModel).order_by(asc("username")),
            count_stmt=select(func.count(UserModel.id)),
        )
        return await paginator(page_size=page_size, current_page=current_page)

    @get("/{user_id:uuid}")
    async def get(self, user_id: UUID, users_repo: UserRepository) -> UserReadSchema:
        obj = await users_repo.get(user_id)
        return UserReadSchema.model_validate(obj)

    @post("/")
    async def create(
        self, data: UserCreateSchema, users_repo: UserRepository
    ) -> UserReadSchema:
        raw_obj = data.model_dump(exclude_unset=True)
        if raw_obj.get("addresses"):
            raw_addrs = []
            for raw_addr in raw_obj["addresses"]:
                raw_addrs.append(AddressModel(**raw_addr))
            raw_obj["addresses"] = raw_addrs
        obj = await users_repo.add(UserModel(**raw_obj))
        await users_repo.session.commit()
        obj = await users_repo.get(obj.id)
        return UserReadSchema.model_validate(obj)

    @put("/{user_id:uuid}")
    async def update(
        self, user_id: UUID, data: UserUpdateSchema, users_repo: UserRepository
    ) -> UserReadSchema:
        raw_obj = data.model_dump(exclude_unset=True)
        raw_obj.update({"id": user_id})
        if raw_obj.get("addresses"):
            raw_addrs = []
            for raw_addr in raw_obj["addresses"]:
                raw_addrs.append(AddressModel(**raw_addr))
            raw_obj["addresses"] = raw_addrs
        obj = await users_repo.update(UserModel(**raw_obj))
        await users_repo.session.commit()
        return UserReadSchema.model_validate(obj)

    @delete("/{user_id:uuid}")
    async def delete(self, user_id: UUID, users_repo: UserRepository) -> None:
        await users_repo.delete(user_id)
        await users_repo.session.commit()
