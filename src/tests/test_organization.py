from litestar.testing import AsyncTestClient
from litestar import Litestar

from organization.models import CountryModel, CityModel


async def test_get_list_counties(test_client: AsyncTestClient[Litestar], auth_header):
    response = await test_client.get("/countries", headers=auth_header)
    assert response.status_code == 200


async def test_get_country(
    test_client: AsyncTestClient[Litestar], country: CountryModel, auth_header
):
    response = await test_client.get(f"/countries/{country.id}", headers=auth_header)
    assert response.status_code == 200


async def test_create_country(test_client: AsyncTestClient[Litestar], auth_header):
    response = await test_client.post(
        "/countries", json={"name": "Country New"}, headers=auth_header
    )
    assert response.status_code == 201


async def test_update_country(
    test_client: AsyncTestClient[Litestar], country: CountryModel, auth_header
):
    response = await test_client.put(
        f"/countries/{country.id}",
        json={"name": "Country New Updated"},
        headers=auth_header,
    )
    assert response.status_code == 200


async def test_delete_country(
    test_client: AsyncTestClient[Litestar], country: CountryModel, auth_header
):
    response = await test_client.delete(f"/countries/{country.id}", headers=auth_header)
    assert response.status_code == 204


async def test_get_list_cities(test_client: AsyncTestClient[Litestar], auth_header):
    response = await test_client.get("/cities", headers=auth_header)
    assert response.status_code == 200


async def test_get_city(
    test_client: AsyncTestClient[Litestar], city: CityModel, auth_header
):
    response = await test_client.get(f"/cities/{city.id}", headers=auth_header)
    assert response.status_code == 200


async def test_create_city(
    test_client: AsyncTestClient[Litestar], country: CountryModel, auth_header
):
    response = await test_client.post(
        "/cities",
        json={"name": "City New", "country_id": str(country.id)},
        headers=auth_header,
    )
    assert response.status_code == 201


async def test_update_city(
    test_client: AsyncTestClient[Litestar], city: CityModel, auth_header
):
    response = await test_client.put(
        f"/cities/{city.id}", json={"name": "City New Updated"}, headers=auth_header
    )
    assert response.status_code == 200


async def test_delete_city(
    test_client: AsyncTestClient[Litestar], city: CityModel, auth_header
):
    response = await test_client.delete(f"/cities/{city.id}", headers=auth_header)
    assert response.status_code == 204
