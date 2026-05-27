from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.api import analytics, auth, repositories, reviews, stream
from src.config import get_settings
from src.core.redis import close_redis
from src.observability.logging import configure_logging, get_logger
from src.observability.metrics import metrics_router
from src.webhooks.router import router as webhooks_router

settings = get_settings()
configure_logging(settings.log_level, settings.service_name)
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("api.startup", env=settings.environment)
    try:
        yield
    finally:
        await close_redis()
        log.info("api.shutdown")


app = FastAPI(
    title="Lineage API",
    version="0.1.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", tags=["meta"])
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz", tags=["meta"])
async def readyz() -> dict[str, str]:
    return {"status": "ready"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(repositories.router, prefix="/api/repositories", tags=["repositories"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(stream.router, prefix="/api/stream", tags=["stream"])

if settings.prometheus_enabled:
    app.include_router(metrics_router, tags=["meta"])
