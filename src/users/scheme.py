from uuid import UUID
from pydantic import BaseModel

from organization.scheme import CityReadSchema


class UserReadSchema(BaseModel):
    id: UUID
    email: str
    username: str
    addresses: list["AddressSchema"]

    model_config = {
        "from_attributes": True,
    }


class UserCreateSchema(BaseModel):
    email: str
    username: str


class UserUpdateSchema(BaseModel):
    email: str | None = None
    username: str | None = None


class AddressSchema(BaseModel):
    city: CityReadSchema
    id: UUID

    model_config = {
        "from_attributes": True,
    }
