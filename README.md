# Adaptive Code Review Agent

AI-powered code review system that learns your team's standards over time and delivers context-aware PR feedback.

Listens to GitHub PR webhooks, analyzes diffs semantically, retrieves similar past reviews from a vector store, and generates structured file-level feedback with severity rankings. Improves continuously from accepted/dismissed feedback.

**Stack:** Next.js (web) + FastAPI (api)

---

## Running with Docker

Secrets are loaded from `apps/api/.env` (gitignored). Copy `apps/api/.env.example` first:

```bash
cp apps/api/.env.example apps/api/.env
# fill in GITHUB_OAUTH_*, GITHUB_APP_*, GOOGLE_API_KEY, JWT_SECRET, GITHUB_WEBHOOK_SECRET
```

### Full stack (production build)

```bash
make up         # build + start web, api, worker, postgres, redis, qdrant, prometheus, grafana
make ps         # list containers
make logs       # tail all logs
make down       # stop stack
make clean      # down + remove volumes (wipes db)
```

### Full stack (hot-reload dev)

```bash
make up-dev     # mounts source, runs uvicorn --reload + pnpm dev + celery worker
```

### Infra only (db / redis / qdrant / prometheus / grafana)

Use when running `web` and `api` directly on the host:

```bash
make infra-up
make infra-logs
make infra-down
```

### One-off commands

```bash
# Apply migrations manually
docker compose -f infra/docker-compose.yml run --rm migrate

# Open a shell in the API container
docker compose -f infra/docker-compose.yml exec api bash

# Tail worker logs only
docker compose -f infra/docker-compose.yml logs -f worker

# Rebuild a single service
docker compose -f infra/docker-compose.yml build api
```

### Service URLs

| Service    | URL                       |
| ---------- | ------------------------- |
| Web        | http://localhost:3000     |
| API        | http://localhost:8000     |
| Postgres   | localhost:5432            |
| Redis      | localhost:6379            |
| Qdrant     | http://localhost:6333     |
| Prometheus | http://localhost:9090     |
| Grafana    | http://localhost:3001     |

Grafana login: `admin` / `admin`.
