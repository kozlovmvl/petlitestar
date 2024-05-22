import uuid
from litestar import Controller, post, get
from litestar.status_codes import HTTP_200_OK

from auth.scheme import LoginRequestSchema, LoginResponseSchema
from auth.models import TokenModel


class AuthController(Controller):
    path = "auth"

    @post("/login", status_code=HTTP_200_OK)
    async def login(self, data: LoginRequestSchema) -> LoginResponseSchema:
        token = TokenModel.create(user_id=uuid.uuid4())
        encoded = TokenModel.encode(token)
        return LoginResponseSchema(token=encoded)

    @get("/logout")
    async def logout(self) -> None:
        pass
