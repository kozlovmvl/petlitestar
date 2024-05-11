from uuid import UUID, uuid4
from litestar import Controller, get, post, delete

from .scheme import UserReadSchema, UserCreateSchema, UserUpdateSchema


class UserController(Controller):
    @get("/")
    async def get_list(self) -> list[UserReadSchema]:
        return [UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")]

    @get("/{user_id:UUID}")
    async def get(self, user_id: UUID) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @post("/")
    async def create(self, data: UserCreateSchema) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @post("/{user_id:UUID}")
    async def update(self, user_id: UUID, data: UserUpdateSchema) -> UserReadSchema:
        return UserReadSchema(id=uuid4(), email="user1@mail.ru", username="user1")

    @delete("/{user_id:UUID}")
    async def delete(self, user_id: UUID) -> None:
        pass
