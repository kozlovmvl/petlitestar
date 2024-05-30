import os
import sys

sys.path.append(os.path.dirname(__file__))

from litestar import Litestar
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend

from db import on_startup, sqlalchemy_plugin

from auth.controller import AuthController
from chats.controllers import ChatController, MessageController, chat_handler
from organization.controllers import CityController, CountryController
from users.controllers import UserController

app = Litestar(
    route_handlers=[
        AuthController,
        ChatController,
        MessageController,
        chat_handler,
        CityController,
        CountryController,
        UserController,
    ],
    on_startup=[on_startup],
    # on_shutdown=[on_shutdown],
    plugins=[
        sqlalchemy_plugin,
        ChannelsPlugin(
            backend=MemoryChannelsBackend(),
            arbitrary_channels_allowed=True,
            # channels=["chats"],
            create_ws_route_handlers=True,
        ),
    ],
    # middleware=[DefineMiddleware(JWTAuthMiddleware, exclude=["schema", "auth"])],
    debug=True,
)
