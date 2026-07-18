from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.redis_client import redis_client
from app.routers import jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client.ping()
    yield


app = FastAPI(title="Conductor", lifespan=lifespan)
app.include_router(jobs.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
