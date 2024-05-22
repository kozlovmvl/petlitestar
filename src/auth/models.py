from jose import jwt
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer
from auth.settings import TOKEN_LIFE_DURATION, JWT_SECRET, JWT_ALGORITHM


class TokenModel(BaseModel):
    date_expires: datetime
    user_id: UUID

    @field_serializer("date_expires")
    def date_expires_serialize(self, value: datetime, info):
        return value.isoformat("T")

    @field_serializer("user_id")
    def user_id_serialize(self, value: UUID, info):
        return str(value)

    def is_expired(self) -> bool:
        return datetime.now() > self.date_expires

    @classmethod
    def create(cls, user_id: UUID) -> "TokenModel":
        return cls(date_expires=datetime.now() + TOKEN_LIFE_DURATION, user_id=user_id)

    @staticmethod
    def encode(token: "TokenModel") -> str:
        return jwt.encode(token.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)
