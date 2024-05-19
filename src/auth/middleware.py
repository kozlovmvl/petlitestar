from jose import jwt
from litestar.connection import ASGIConnection
from litestar.middleware import AuthenticationResult, AbstractAuthenticationMiddleware

API_KEY_HEADER = "X-API-KEY"


class JWTAuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        auth_header = connection.headers.get(API_KEY_HEADER)
        data = jwt.decode(auth_header, "secret", algorithms=["HS256"])
        print(data)
        return AuthenticationResult(user=None, auth=None)
