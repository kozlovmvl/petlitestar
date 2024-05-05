from litestar import Litestar, get

@get("/login")
async def login() -> dict[str, str]:
    return {"token": "token"}

app = Litestar([login])
