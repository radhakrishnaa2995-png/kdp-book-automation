from __future__ import annotations

import json
import os
import secrets
from dataclasses import dataclass
from typing import Iterable, List
from urllib import error, request


OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_SECRET_NAME = "OPENROUTER_API_KEY"
OPENROUTER_MODEL_ENV = "OPENROUTER_MODEL"
OPENROUTER_API_BASE_ENV = "OPENROUTER_API_BASE"
OPENROUTER_REFERER_ENV = "OPENROUTER_HTTP_REFERER"
OPENROUTER_TITLE_ENV = "OPENROUTER_APP_TITLE"


@dataclass(frozen=True)
class ApiTheme:
    theme: str
    words: List[str]


def _coerce_payload(payload: object) -> List[ApiTheme]:
    if isinstance(payload, dict):
        payload = payload.get("themes", [])
    if not isinstance(payload, list):
        raise ValueError("Theme API response must be a list or an object with a 'themes' list.")

    themes: List[ApiTheme] = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Each theme entry returned by the API must be an object.")
        theme = item.get("theme")
        words = item.get("words")
        if not isinstance(theme, str) or not isinstance(words, list):
            raise ValueError("Each theme entry must contain 'theme' (str) and 'words' (list).")
        clean_words = [word for word in words if isinstance(word, str)]
        themes.append(ApiTheme(theme=theme, words=clean_words))
    return themes


def _extract_json_payload(content: str) -> object:
    content = content.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if len(lines) >= 3:
            content = "\n".join(lines[1:-1]).strip()
    return json.loads(content)


def fetch_themes(
    api_url: str,
    count: int,
    min_words: int,
    max_words: int,
    excluded_themes: Iterable[str],
    excluded_words: Iterable[str],
    uniqueness_token: str | None = None,
    timeout: float = 30.0,
) -> List[ApiTheme]:
    payload = {
        "count": count,
        "min_words": min_words,
        "max_words": max_words,
        "excluded_themes": list(excluded_themes),
        "excluded_words": list(excluded_words),
        "uniqueness_token": uniqueness_token or secrets.token_hex(8),
    }
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(http_request, timeout=timeout) as response:
        data = response.read().decode("utf-8")
    parsed = json.loads(data)
    return _coerce_payload(parsed)


def fetch_themes_from_openrouter(
    count: int,
    min_words: int,
    max_words: int,
    excluded_themes: Iterable[str],
    excluded_words: Iterable[str],
    api_key: str | None = None,
    model: str | None = None,
    api_base: str | None = None,
    uniqueness_token: str | None = None,
    timeout: float = 60.0,
) -> List[ApiTheme]:
    api_key = api_key or os.getenv(OPENROUTER_SECRET_NAME)
    if not api_key:
        raise ValueError(
            f"Missing OpenRouter API key. Set the {OPENROUTER_SECRET_NAME} environment variable or pass api_key explicitly."
        )

    model = model or os.getenv(OPENROUTER_MODEL_ENV, "openai/gpt-4o-mini")
    api_base = api_base or os.getenv(OPENROUTER_API_BASE_ENV, OPENROUTER_API_BASE)
    uniqueness_token = uniqueness_token or secrets.token_hex(8)

    instruction = {
        "task": "Generate unique word-search themes.",
        "uniqueness_token": uniqueness_token,
        "requirements": {
            "theme_count": count,
            "min_words_per_theme": min_words,
            "max_words_per_theme": max_words,
            "theme_rules": [
                "Every theme title must be different.",
                "Avoid generic repeats of excluded themes and common catalog topics.",
                "Theme titles should be kid-friendly and book-safe.",
                "Invent fresh, specific concepts for this run instead of reusing common stock themes.",
            ],
            "word_rules": [
                "Every word must be alphabetic only.",
                "Use uppercase-friendly single tokens without punctuation.",
                "Every word must be between 3 and 15 letters long.",
                "Do not repeat excluded words.",
                "Keep words related strongly to the theme.",
                "Choose words that feel fresh for this run instead of defaulting to common catalog words.",
            ],
        },
        "excluded_themes": list(excluded_themes),
        "excluded_words": list(excluded_words),
        "response_shape": {
            "themes": [
                {
                    "theme": "THEME NAME",
                    "words": ["WORD1", "WORD2", "WORD3"]
                }
            ]
        },
    }

    strict_body = {
        "model": model,
        "temperature": 1.15,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You create brand-new word-search themes and word lists. "
                    "Return valid JSON only, with no markdown and no explanation."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(instruction),
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "theme_batch",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "themes": {
                            "type": "array",
                            "minItems": count,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "theme": {"type": "string"},
                                    "words": {
                                        "type": "array",
                                        "minItems": min_words,
                                        "maxItems": max_words,
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": ["theme", "words"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["themes"],
                    "additionalProperties": False,
                },
            },
        },
    }
    fallback_body = {
        "model": model,
        "temperature": 1.15,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You create brand-new word-search themes and word lists. "
                    "Return valid JSON only, with no markdown and no explanation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{json.dumps(instruction)}\n"
                    "Return exactly one JSON object shaped like "
                    '{"themes":[{"theme":"THEME NAME","words":["WORD1","WORD2","WORD3"]}]}.'
                ),
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    referer = os.getenv(OPENROUTER_REFERER_ENV)
    title = os.getenv(OPENROUTER_TITLE_ENV)
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title

    def _send(body: dict) -> dict:
        http_request = request.Request(
            api_base,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with request.urlopen(http_request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    try:
        payload = _send(strict_body)
    except error.HTTPError as exc:
        if exc.code not in {400, 404, 422}:
            raise
        payload = _send(fallback_body)

    content = payload["choices"][0]["message"]["content"]
    parsed = _extract_json_payload(content)
    return _coerce_payload(parsed)
