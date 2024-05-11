from uuid import UUID, uuid4
from litestar import Controller, get, post, delete
from litestar.di import Provide
from pydantic import TypeAdapter

from .models import UserRepository, provide_user_repository

from .scheme import UserReadSchema, UserCreateSchema, UserUpdateSchema


class UserController(Controller):
    dependencies = {"users_repo": Provide(provide_user_repository)}

    @get("/")
    async def get_list(self, users_repo: UserRepository) -> list[UserReadSchema]:
        result = await users_repo.list()
        type_adapter = TypeAdapter(list[UserReadSchema])
        return type_adapter.validate_python(result)

    @get("/{user_id:str}")
    async def get(self, user_id: UUID) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @post("/")
    async def create(self, data: UserCreateSchema) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @post("/{user_id:str}")
    async def update(self, user_id: UUID, data: UserUpdateSchema) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @delete("/{user_id:str}")
    async def delete(self, user_id: UUID) -> None:
        pass
