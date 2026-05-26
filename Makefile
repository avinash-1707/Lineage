.DEFAULT_GOAL := help
SHELL := /bin/bash

COMPOSE      := docker compose -f infra/docker-compose.yml
COMPOSE_DEV  := docker compose -f infra/docker-compose.yml -f infra/docker-compose.dev.yml

WEB_DIR := apps/web
API_DIR := apps/api

# ----------------------------------------------------------------------------
# help
# ----------------------------------------------------------------------------
.PHONY: help
help:
	@echo "Lineage — local dev targets"
	@echo ""
	@echo "  make install       install web + api deps"
	@echo "  make web           run Next.js dev server (host)"
	@echo "  make api           run FastAPI dev server (host)"
	@echo "  make dev           run web + api concurrently (host)"
	@echo ""
	@echo "  make infra-up      start postgres/redis/qdrant/prometheus/grafana"
	@echo "  make infra-down    stop infra services"
	@echo "  make infra-logs    tail infra logs"
	@echo ""
	@echo "  make up            full stack via docker compose (prod build)"
	@echo "  make up-dev        full stack with hot-reload overrides"
	@echo "  make down          stop full stack"
	@echo "  make logs          tail all stack logs"
	@echo "  make build         build web + api images"
	@echo "  make ps            list stack containers"
	@echo "  make clean         down + remove volumes"

# ----------------------------------------------------------------------------
# install / host dev
# ----------------------------------------------------------------------------
.PHONY: install install-web install-api
install: install-web install-api

install-web:
	cd $(WEB_DIR) && pnpm install

install-api:
	cd $(API_DIR) && uv sync --extra dev

.PHONY: web api dev
web:
	cd $(WEB_DIR) && pnpm dev

api:
	cd $(API_DIR) && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

dev:
	@echo "starting api + web (Ctrl-C stops both)"
	@trap 'kill 0' INT TERM EXIT; \
	  ( cd $(API_DIR) && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload ) & \
	  ( cd $(WEB_DIR) && pnpm dev ) & \
	  wait

# ----------------------------------------------------------------------------
# infra only (postgres, redis, qdrant, prometheus, grafana)
# ----------------------------------------------------------------------------
INFRA_SVCS := postgres redis qdrant prometheus grafana

.PHONY: infra-up infra-down infra-logs
infra-up:
	$(COMPOSE) up -d $(INFRA_SVCS)

infra-down:
	$(COMPOSE) stop $(INFRA_SVCS)

infra-logs:
	$(COMPOSE) logs -f $(INFRA_SVCS)

# ----------------------------------------------------------------------------
# full stack via compose
# ----------------------------------------------------------------------------
.PHONY: up up-dev down logs build ps clean
up:
	$(COMPOSE) up -d --build

up-dev:
	$(COMPOSE_DEV) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

build:
	$(COMPOSE) build

ps:
	$(COMPOSE) ps

clean:
	$(COMPOSE) down -v
