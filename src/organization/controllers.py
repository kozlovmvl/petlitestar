from uuid import UUID
from litestar import Controller, get, post, delete
from litestar.di import Provide
from pydantic import TypeAdapter
from sqlalchemy import asc, select

from organization.models import CityModel, CityRepository, provide_city_repository
from organization.scheme import CityReadSchema, CityCreateSchema, CityUpdateSchema


class CityController(Controller):
    path = "cities"
    dependencies = {"cities_repo": Provide(provide_city_repository)}

    @get("/")
    async def get_list(self, cities_repo: CityRepository) -> list[CityReadSchema]:
        result = await cities_repo.list(
            statement=select(CityModel).order_by(asc("name"))
        )
        type_adapter = TypeAdapter(list[CityReadSchema])
        return type_adapter.validate_python(result)

    @get("/{city_id:uuid}")
    async def get(self, city_id: UUID, cities_repo: CityRepository) -> CityReadSchema:
        obj = await cities_repo.get(city_id)
        return CityReadSchema.model_validate(obj)

    @post("/")
    async def create(
        self, data: CityCreateSchema, cities_repo: CityRepository
    ) -> CityReadSchema:
        obj = await cities_repo.add(CityModel(**data.model_dump(exclude_unset=True)))
        await cities_repo.session.commit()
        return CityReadSchema.model_validate(obj)

    @post("/{city_id:uuid}")
    async def update(
        self, city_id: UUID, data: CityUpdateSchema, cities_repo: CityRepository
    ) -> CityReadSchema:
        raw_obj = data.model_dump(exclude_unset=True)
        raw_obj.update({"id": city_id})
        obj = await cities_repo.update(CityModel(**raw_obj))
        await cities_repo.session.commit()
        return CityReadSchema.model_validate(obj)

    @delete("/{city_id:uuid}")
    async def delete(self, city_id: UUID, cities_repo: CityRepository) -> None:
        await cities_repo.delete(city_id)
        await cities_repo.session.commit()
