from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

from .db import on_startup, sqlalchemy_config

from .users.controllers import UserController

app = Litestar(
    route_handlers=[UserController],
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
)
