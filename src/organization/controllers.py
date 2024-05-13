from litestar import Controller, get
from litestar.di import Provide
from pydantic import TypeAdapter

from organization.models import CityRepository, provide_city_repository
from organization.scheme import CityReadSchema


class CityController(Controller):
    path = "cities"
    dependencies = {"cities_repo": Provide(provide_city_repository)}

    @get("/")
    async def get_list(self, cities_repo: CityRepository) -> list[CityReadSchema]:
        result = await cities_repo.list()
        type_adapter = TypeAdapter(list[CityReadSchema])
        return type_adapter.validate_python(result)

    # @get("/{city_id:uuid}")
    # async def get(self, city_id: UUID) -> CityReadSchema:
    #     pass
    #
    # @post("/")
    # async def create(self, data: CityCreateSchema) -> CityReadSchema:
    #     pass
    #
    # @post("/{city_id:uuid}")
    # async def update(self, city_id: UUID, data: CityUpdateSchema) -> CityReadSchema:
    #     pass
    #
    # @delete("/{city_id:uuid}")
    # async def delete(self, city_id: UUID) -> None:
    #     pass
