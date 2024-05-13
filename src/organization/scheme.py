from uuid import UUID
from pydantic import BaseModel


class CityReadSchema(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class CityCreateSchema(BaseModel):
    name: str


class CityUpdateSchema(BaseModel):
    name: str
