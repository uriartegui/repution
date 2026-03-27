from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.companies import router as companies_router
from app.api.v1.mentions import router as mentions_router
from app.api.v1.collect import router as collect_router
from app.core.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler(interval_hours=1)
    yield
    stop_scheduler()


app = FastAPI(title="Repution API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies_router, prefix="/api/v1")
app.include_router(mentions_router, prefix="/api/v1")
app.include_router(collect_router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok", "version": "0.1.0"}
