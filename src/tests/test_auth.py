async def test_login(test_client):
    response = await test_client.post(
        "/auth/login", json={"username": "username", "password": "password"}
    )
    assert response.status_code == 200
