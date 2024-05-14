from uuid import UUID
from pydantic import BaseModel

from organization.scheme import CityReadSchema


class UserReadSchema(BaseModel):
    id: UUID
    email: str
    username: str
    addresses: list["AddressReadSchema"]

    model_config = {
        "from_attributes": True,
    }


class UserCreateSchema(BaseModel):
    email: str
    username: str
    addresses: list["AddressCreateSchema"] | None = None


class UserUpdateSchema(BaseModel):
    email: str | None = None
    username: str | None = None
    addresses: list["AddressCreateSchema"] | None = None


class AddressReadSchema(BaseModel):
    city: CityReadSchema

    model_config = {
        "from_attributes": True,
    }


class AddressCreateSchema(BaseModel):
    city_id: UUID
