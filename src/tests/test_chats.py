from litestar.testing import AsyncTestClient
from litestar import Litestar

from chats.models import ChatModel, MessageModel
from users.models import UserModel


async def test_get_list_chats(test_client: AsyncTestClient[Litestar], auth_header):
    response = await test_client.get(
        "/chats", headers=auth_header, params={"page_size": 10, "current_page": 0}
    )
    assert response.status_code == 200


async def get_list_messages(
    test_client: AsyncTestClient[Litestar], auth_header, chat: ChatModel
):
    response = await test_client.get(
        f"/chats/messages/{chat.id}",
        headers=auth_header,
        params={"page_size": 10, "current_page": 0},
    )
    assert response.status_code == 200


async def test_create_message(
    test_client: AsyncTestClient[Litestar],
    auth_header,
    chat: ChatModel,
    user: UserModel,
):
    data = {
        "chat_id": str(chat.id),
        "author_id": str(user.id),
        "text": "text",
    }
    response = await test_client.post("/chats/messages", headers=auth_header, json=data)
    assert response.status_code == 201


async def test_update_message(
    test_client: AsyncTestClient[Litestar], auth_header, message: MessageModel
):
    data = {
        "text": "new text",
    }
    response = await test_client.put(
        f"/chats/messages/{message.id}", headers=auth_header, json=data
    )
    assert response.status_code == 200


async def test_delete_message(
    test_client: AsyncTestClient[Litestar], auth_header, message: MessageModel
):
    response = await test_client.delete(
        f"/chats/messages/{message.id}", headers=auth_header
    )
    assert response.status_code == 204
