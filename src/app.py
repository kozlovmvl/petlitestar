import os
import sys

sys.path.append(os.path.dirname(__file__))

from litestar import Litestar

from db import on_startup, sqlalchemy_plugin

from auth.controller import AuthController
from chats.controllers import ChatController
from organization.controllers import CityController, CountryController
from users.controllers import UserController

app = Litestar(
    route_handlers=[
        AuthController,
        ChatController,
        CityController,
        CountryController,
        UserController,
    ],
    on_startup=[on_startup],
    # on_shutdown=[on_shutdown],
    plugins=[sqlalchemy_plugin],
    # middleware=[DefineMiddleware(JWTAuthMiddleware, exclude=["schema", "auth"])],
    debug=True,
)
