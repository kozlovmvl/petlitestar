from uuid import UUID
from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: UUID
    email: str
    username: str

    model_config = {"from_attributes": True}


class UserCreateSchema(BaseModel):
    email: str
    username: str


class UserUpdateSchema(BaseModel):
    email: str | None = None
    username: str | None = None
