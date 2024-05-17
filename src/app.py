import os
import sys

sys.path.append(os.path.dirname(__file__))

from litestar import Litestar

from db import on_startup, on_shutdown, sqlalchemy_plugin

from organization.controllers import CityController, CountryController
from users.controllers import UserController

app = Litestar(
    route_handlers=[
        CityController,
        CountryController,
        UserController,
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    plugins=[sqlalchemy_plugin],
    debug=True,
)
