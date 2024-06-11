from litestar.testing import AsyncTestClient
from litestar import Litestar

from organization.models import CityModel
from users.models import UserModel


async def test_get_list_users(test_client: AsyncTestClient[Litestar], auth_header):
    response = await test_client.get(
        "/users", headers=auth_header, params={"page_size": 10, "current_page": 0}
    )
    assert response.status_code == 200


async def test_get_user(
    test_client: AsyncTestClient[Litestar], auth_header, user: UserModel
):
    response = await test_client.get(f"/users/{user.id}", headers=auth_header)
    assert response.status_code == 200


async def test_create_user(
    test_client: AsyncTestClient[Litestar], auth_header, city: CityModel
):
    data = {
        "username": "username",
        "email": "username@test.test",
        "addresses": [{"city_id": str(city.id)}],
    }
    response = await test_client.post("/users", headers=auth_header, json=data)
    assert response.status_code == 201


async def test_update_user(
    test_client: AsyncTestClient[Litestar], auth_header, user: UserModel
):
    data = {
        "username": "newuser",
        "email": "newuser@test.test",
    }
    response = await test_client.put(
        f"/users/{user.id}", headers=auth_header, json=data
    )
    assert response.status_code == 200


async def test_delete_user(
    test_client: AsyncTestClient[Litestar], auth_header, user: UserModel
):
    response = await test_client.delete(f"/users/{user.id}", headers=auth_header)
    assert response.status_code == 204
