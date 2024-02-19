from fastapi import FastAPI
from .routers import events, reservations, users
from .database import init_db


app = FastAPI()


async def app_lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield


app.lifespan = app_lifespan

app.include_router(events.router)
app.include_router(reservations.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
