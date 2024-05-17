from uuid import UUID
from litestar import Controller, get, post, delete, put
from litestar.di import Provide
from pydantic import TypeAdapter
from sqlalchemy import asc, select

from users.models import (
    AddressModel,
    UserModel,
    UserRepository,
    provide_user_repository,
)
from users.scheme import UserReadSchema, UserCreateSchema, UserUpdateSchema


class UserController(Controller):
    path = "users"
    dependencies = {"users_repo": Provide(provide_user_repository)}

    @get("/")
    async def get_list(self, users_repo: UserRepository) -> list[UserReadSchema]:
        objs = await users_repo.list(
            statement=select(UserModel).order_by(asc("username"))
        )
        type_adapter = TypeAdapter(list[UserReadSchema])
        return type_adapter.validate_python(objs)

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
