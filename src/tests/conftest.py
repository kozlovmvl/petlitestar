import os
from collections.abc import AsyncIterator
from litestar.testing import AsyncTestClient
from litestar import Litestar
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from organization.models import (
    CountryModel,
    CityModel,
    CountryRepository,
    CityRepository,
)

from app import app


@pytest.fixture()
async def session_factory():
    engine = create_async_engine(
        "postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(
            **os.environ
        ),
        future=True,
    )
    yield async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture()
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app) as client:
        yield client


@pytest.fixture()
async def country_repository(session_factory) -> AsyncIterator[CountryRepository]:
    async with session_factory() as db_session:
        yield CountryRepository(session=db_session)


@pytest.fixture()
async def city_repository(session_factory) -> AsyncIterator[CityRepository]:
    async with session_factory() as db_session:
        yield CityRepository(session=db_session)


@pytest.fixture()
async def country(country_repository) -> CountryModel:
    obj = await country_repository.add(CountryModel(name="Country"))
    await country_repository.session.commit()
    return obj


@pytest.fixture()
async def city(city_repository, country) -> CityModel:
    obj = await city_repository.add(CityModel(name="City", country_id=country.id))
    await city_repository.session.commit()
    return obj
