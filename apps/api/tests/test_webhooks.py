from __future__ import annotations

import hashlib
import hmac
import json

import pytest
from httpx import AsyncClient


def _sign(payload: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


@pytest.mark.asyncio
async def test_webhook_rejects_bad_signature(client: AsyncClient) -> None:
    r = await client.post(
        "/webhooks/github",
        content=b"{}",
        headers={"X-GitHub-Event": "ping", "X-Hub-Signature-256": "sha256=deadbeef"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_webhook_accepts_ping(client: AsyncClient, monkeypatch) -> None:
    from src.config import get_settings

    settings = get_settings()
    secret = settings.github_webhook_secret.get_secret_value()
    body = json.dumps({"zen": "hi"}).encode()
    r = await client.post(
        "/webhooks/github",
        content=body,
        headers={
            "X-GitHub-Event": "ping",
            "X-Hub-Signature-256": _sign(body, secret),
        },
    )
    assert r.status_code == 202
    assert r.json()["status"] in {"ignored", "queued"}
