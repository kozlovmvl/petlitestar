from pydantic import BaseModel


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class LoginResponseSchema(BaseModel):
    token: str
