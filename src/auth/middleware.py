from jose import jwt
from jose.exceptions import JWTError
from litestar.connection import ASGIConnection
from litestar.middleware import AuthenticationResult, AbstractAuthenticationMiddleware
from litestar.exceptions import NotAuthorizedException
from auth.models import TokenModel

from auth.settings import API_KEY_HEADER, JWT_SECRET, JWT_ALGORITHM


class JWTAuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        auth_header = connection.headers.get(API_KEY_HEADER, "")
        try:
            data = jwt.decode(auth_header, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except JWTError:
            raise NotAuthorizedException
        token = TokenModel.model_validate(data)
        if token.is_expired():
            raise NotAuthorizedException
        return AuthenticationResult(user=None, auth=None)
