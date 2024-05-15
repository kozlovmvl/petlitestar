from uuid import UUID
from pydantic import BaseModel


class CountryReadSchema(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class CountryCreateSchema(BaseModel):
    name: str


class CountryUpdateSchema(BaseModel):
    name: str


class CityReadSchema(BaseModel):
    id: UUID
    name: str
    country: CountryReadSchema

    model_config = {"from_attributes": True}


class CityCreateSchema(BaseModel):
    name: str


class CityUpdateSchema(BaseModel):
    name: str
