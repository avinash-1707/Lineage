from __future__ import annotations

from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

metrics_router = APIRouter()

webhook_received = Counter(
    "lineage_webhook_received_total",
    "GitHub webhooks received.",
    ["event"],
)

reviews_run = Counter(
    "lineage_reviews_run_total",
    "Review tasks executed.",
    ["status"],
)

review_latency = Histogram(
    "lineage_review_latency_seconds",
    "End-to-end PR review latency.",
    buckets=(1, 5, 10, 30, 60, 120, 300, 600),
)

memory_hits = Histogram(
    "lineage_memory_hits",
    "Memory hits per review.",
    buckets=(0, 1, 2, 5, 10, 20, 50),
)


@metrics_router.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
