"""Thin, testable wrapper around the Google GenAI SDK.

Centralizes:
  * client construction (single shared `genai.Client`)
  * retry/timeout policy
  * structured JSON generation
  * batched embedding helpers

Callers should depend on `GeminiClient` rather than reaching into `google.genai`
so the surface stays small and swappable.
"""

from __future__ import annotations

import asyncio
import json
from functools import lru_cache
from typing import Any

from google import genai
from google.genai import types as genai_types
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.config import Settings, get_settings
from src.observability.logging import get_logger

log = get_logger(__name__)


class GeminiConfigError(RuntimeError):
    """Raised when Gemini is used without a configured API key."""


class GeminiClient:
    """Async-friendly façade over `google.genai.Client`.

    The underlying SDK is sync; we run calls in a worker thread via
    `asyncio.to_thread` so the event loop is never blocked.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        if self._settings.google_api_key is None:
            raise GeminiConfigError("GOOGLE_API_KEY is not configured")
        self._client = genai.Client(
            api_key=self._settings.google_api_key.get_secret_value()
        )

    # ------------------------------------------------------------------ embeddings
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    async def embed(self, texts: list[str], *, task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        if not texts:
            return []

        def _call() -> list[list[float]]:
            resp = self._client.models.embed_content(
                model=self._settings.embedding_model,
                contents=texts,
                config=genai_types.EmbedContentConfig(task_type=task_type),
            )
            return [list(e.values) for e in resp.embeddings]

        return await asyncio.to_thread(_call)

    async def embed_one(self, text: str, *, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
        result = await self.embed([text], task_type=task_type)
        return result[0]

    # ---------------------------------------------------------------- generation
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    async def generate_text(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        cfg = genai_types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature if temperature is not None else self._settings.gemini_temperature,
            max_output_tokens=max_output_tokens or self._settings.gemini_max_output_tokens,
        )

        def _call() -> str:
            resp = self._client.models.generate_content(
                model=self._settings.gemini_model,
                contents=prompt,
                config=cfg,
            )
            return resp.text or ""

        return await asyncio.to_thread(_call)

    async def generate_json(
        self,
        prompt: str,
        *,
        schema: dict[str, Any] | None = None,
        system_instruction: str | None = None,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> Any:
        cfg = genai_types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature if temperature is not None else self._settings.gemini_temperature,
            max_output_tokens=max_output_tokens or self._settings.gemini_max_output_tokens,
            response_mime_type="application/json",
            response_schema=schema,
        )

        def _call() -> str:
            resp = self._client.models.generate_content(
                model=self._settings.gemini_model,
                contents=prompt,
                config=cfg,
            )
            return resp.text or "null"

        raw = await asyncio.to_thread(_call)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            log.warning("gemini.invalid_json", raw_preview=raw[:200])
            return None


@lru_cache
def get_gemini_client() -> GeminiClient:
    return GeminiClient()
