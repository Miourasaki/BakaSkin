import os.path

from fastapi import FastAPI
from fastapi.responses import FileResponse
import api
import yggdrasil
from mongo import db

app = FastAPI(
    title="AuthNode"
)

# initialize FastAPI app
from config import init

init(app)

app.include_router(api.router, prefix="/api", tags=["Web API"])

app.include_router(yggdrasil.app, prefix="/api", tags=["Yggdrasil API"])
app.include_router(yggdrasil.app, prefix="/yggdrasil", tags=["Yggdrasil API"])
app.include_router(yggdrasil.app, prefix="/api/yggdrasil", tags=["Yggdrasil API"])


@app.get("/{path:path}")
async def read_root(path: str = "index.html"):
    if path == "":
        path = "index.html"

    path = f"web/dist/{path}"

    if os.path.exists(path):
        return FileResponse(path)
    else:
        return FileResponse("web/dist/index.html")


if __name__ == "__main__":
    db("users").delete_one({"verified": False})
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9999)
