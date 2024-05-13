import os
import sys

sys.path.append(os.path.dirname(__file__))

from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

from .db import on_startup, sqlalchemy_config

from .organization.controllers import CityController
from .users.controllers import UserController

app = Litestar(
    route_handlers=[
        CityController,
        UserController,
    ],
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    debug=True,
)
