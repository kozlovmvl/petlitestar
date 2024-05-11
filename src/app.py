from litestar import Litestar

from .users.controllers import UserController

app = Litestar(route_handlers=[UserController])
