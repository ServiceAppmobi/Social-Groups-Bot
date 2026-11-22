"""Zero-dependency Google Gemini Interactions API client (Python stdlib only)."""

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from config import (
    GEMINI_API_KEY,
    GEMINI_API_VERSION,
    GEMINI_MODEL,
    GEMINI_TIMEOUT_SECONDS,
)

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-3.5-flash-lite"
RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)


class GeminiAPIError(RuntimeError):
    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


class GeminiInteraction:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.id: Optional[str] = raw.get("id")
        self.status: Optional[str] = raw.get("status")
        self.model: Optional[str] = raw.get("model")
        self.steps: List[Dict[str, Any]] = raw.get("steps") or []
        self.usage: Dict[str, Any] = raw.get("usage") or {}

    @property
    def output_text(self) -> Optional[str]:
        trailing_parts: List[str] = []
        found = False
        for step in reversed(self.steps):
            if step.get("type") != "model_output":
                if found:
                    break
                continue
            found = True
            parts = [
                p["text"]
                for p in (step.get("content") or [])
                if p.get("type") == "text" and isinstance(p.get("text"), str)
            ]
            if parts:
                trailing_parts = parts + trailing_parts
        return "".join(trailing_parts) if trailing_parts else None

    def parse_json(self) -> Any:
        text = self.output_text
        if not text:
            raise ValueError("Interaction response contains no text output.")
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if len(lines) >= 2 and lines[-1].strip() == "```":
                cleaned = "\n".join(lines[1:-1]).strip()
        return json.loads(cleaned)


class GeminiClient:
    def __init__(
        self,
        api_key: str = GEMINI_API_KEY,
        default_model: str = GEMINI_MODEL,
        api_version: str = GEMINI_API_VERSION,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = GEMINI_TIMEOUT_SECONDS,
        max_retries: int = 2,
    ):
        self.api_key = (api_key or "").strip()
        self.default_model = (default_model or DEFAULT_MODEL).strip()
        self.api_version = (api_version or "v1").strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def create_interaction(
        self,
        input_data: Any,
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        store: Optional[bool] = False,
        timeout: Optional[int] = None,
    ) -> GeminiInteraction:
        payload: Dict[str, Any] = {"model": model or self.default_model, "input": input_data}
        if system_instruction:
            payload["system_instruction"] = system_instruction
        if generation_config:
            payload["generation_config"] = generation_config
        if response_format:
            payload["response_format"] = response_format
        if store is not None:
            payload["store"] = store
        raw = self._post_json(f"/{self.api_version}/interactions", payload, timeout or self.timeout)
        return GeminiInteraction(raw)

    def create_structured_json(
        self,
        input_data: Any,
        schema: Dict[str, Any],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        temperature: float = 0.4,
    ) -> Tuple[Any, GeminiInteraction]:
        interaction = self.create_interaction(
            input_data=input_data,
            model=model,
            system_instruction=system_instruction,
            generation_config={"temperature": temperature},
            response_format={"type": "text", "mime_type": "application/json", "schema": schema},
            store=False,
        )
        return interaction.parse_json(), interaction

    def health_check(self, model: Optional[str] = None) -> GeminiInteraction:
        return self.create_interaction(
            input_data="Reply with exactly: OK",
            model=model or self.default_model,
            generation_config={"max_output_tokens": 16},
            store=False,
            timeout=min(self.timeout, 20),
        )

    def _post_json(self, path: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
        if not self.is_configured():
            raise GeminiAPIError("GEMINI_API_KEY is not configured.")
        url = f"{self.base_url}{path}"
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        attempts = self.max_retries + 1
        last_error: Optional[Exception] = None
        for attempt in range(attempts):
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                raw_err = exc.read().decode("utf-8", errors="replace")
                msg, code = self._parse_error(raw_err, exc.reason)
                last_error = GeminiAPIError(f"Gemini API HTTP {exc.code}: {msg}", exc.code, code)
                if exc.code in RETRYABLE_STATUS_CODES and attempt < attempts - 1:
                    time.sleep(0.5 * (2 ** attempt))
                    continue
                raise last_error from exc
            except urllib.error.URLError as exc:
                last_error = GeminiAPIError(f"Gemini API network error: {exc.reason}")
                if attempt < attempts - 1:
                    time.sleep(0.5 * (2 ** attempt))
                    continue
                raise last_error from exc
        raise last_error or GeminiAPIError("Gemini API request failed.")

    @staticmethod
    def _parse_error(raw_err: str, fallback: Any) -> Tuple[str, Optional[str]]:
        try:
            parsed = json.loads(raw_err)
            if isinstance(parsed, list) and parsed:
                parsed = parsed[0]
            err = parsed.get("error") if isinstance(parsed, dict) else None
            if isinstance(err, dict):
                return str(err.get("message") or fallback), err.get("status") or err.get("code")
        except Exception:
            pass
        return (raw_err[:300] or str(fallback)), None
