from datetime import datetime
import uuid
from jose import jwt
from litestar import Controller, post, get

from auth.scheme import LoginRequestSchema, LoginResponseSchema
from auth.models import TokenModel


class AuthController(Controller):
    path = "auth"

    @post("/login")
    async def login(self, data: LoginRequestSchema) -> LoginResponseSchema:
        token = TokenModel(date_expires=datetime.now(), user_id=uuid.uuid4())
        encoded = jwt.encode(token.model_dump(), "secret", algorithm="HS256")
        return LoginResponseSchema(token=encoded)

    @get("/logout")
    async def logout(self) -> None:
        pass
