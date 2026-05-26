# Lineage API

FastAPI backend: GitHub webhook receiver, LangGraph PR review agent, Celery workers, Qdrant memory.

## Stack

- **FastAPI** + uvicorn (ASGI, ORJSON responses)
- **SQLAlchemy 2.0** async + asyncpg, Alembic migrations
- **Celery** on Redis (queues: `reviews`, `signals`)
- **LangGraph** review agent (parse → retrieve → match → generate → publish)
- **Qdrant** vector memory of prior review signals
- **Gemini** — `gemini-2.5-flash-lite` LLM, `text-embedding-004` embeddings (768-d)
- **structlog** + Prometheus + SSE event stream

## Layout

```
src/
  main.py            FastAPI app
  config.py          pydantic-settings
  database.py        async engine / session
  webhooks/          GitHub webhook receiver + HMAC verification
  workers/           Celery app + tasks
  agent/             LangGraph nodes + state
  memory/            Qdrant client + embedding helpers
  llm/               Gemini wrapper
  github/            GitHub REST client + diff parser
  models/            SQLAlchemy ORM
  schemas/           Pydantic v2 response models
  services/          DB write layer (upserts)
  api/               REST routes (reviews, repositories, analytics, SSE)
  observability/     structlog + Prometheus
```

## Running locally

```bash
cp .env.example .env
uv pip install -e ".[dev]"
alembic upgrade head
uvicorn src.main:app --reload
celery -A src.workers.celery_app worker -Q reviews,signals --loglevel=info
```

## Tests

```bash
pytest
```

Integration tests rely on testcontainers (Postgres + Redis).
