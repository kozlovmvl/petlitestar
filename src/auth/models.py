from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer


class TokenModel(BaseModel):
    date_expires: datetime
    user_id: UUID

    @field_serializer("date_expires")
    def date_expires_serialize(self, value: datetime, info):
        return value.isoformat("T")

    @field_serializer("user_id")
    def user_id_serialize(self, value: UUID, info):
        return str(value)
