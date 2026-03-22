import sys
from dataclasses import dataclass, field
from typing import Dict, List

from .theme_api import OPENROUTER_MODEL_ENV, fetch_themes, fetch_themes_from_openrouter


@dataclass
class ThemeManager:
    seed: int | None = None
    api_url: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str | None = None
    api_batch_size: int = 24
    api_timeout: float = 30.0
    catalog: Dict[str, List[str]] = field(default_factory=lambda: {k: list(v) for k, v in THEME_CATALOG.items()})

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.used_themes: set[str] = set()
        self.used_words: set[str] = set()
        self.known_words: set[str] = set()
        self._dynamic_fetch_disabled = False
        self.openrouter_api_key = self.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = self.openrouter_model or os.getenv(OPENROUTER_MODEL_ENV, "openai/gpt-4o-mini")
        original_catalog = dict(self.catalog)
        self.catalog = {}
        self._validate_catalog(original_catalog)

    def _register_theme(self, theme: str, words: List[str]) -> None:
        if theme in self.catalog or theme in self.used_themes:
            return
        normalized = []
        for word in words:
            clean = _normalize_word(word)
            if len(clean) < 3:
                return
            if clean in self.known_words or clean in self.used_words:
                return
            normalized.append(clean)
        if len(normalized) < 10:
            return
        self.catalog[theme] = normalized
        self.known_words.update(normalized)

    def _validate_catalog(self, catalog: Dict[str, List[str]]) -> None:
        for theme, words in catalog.items():
            self._register_theme(theme, words)
        if not self.catalog:
            raise ValueError("Theme catalog is empty after validation.")

    def _ensure_dynamic_themes(self, minimum_count: int = 1) -> None:
        if self._dynamic_fetch_disabled or not (self.api_url or self.openrouter_api_key):
            return
        available = [theme for theme in self.catalog if theme not in self.used_themes]
        if len(available) >= minimum_count:
            return

        try:
            if self.api_url:
                generated = fetch_themes(
                    api_url=self.api_url,
                    count=max(self.api_batch_size, minimum_count),
                    min_words=10,
                    max_words=12,
                    excluded_themes=self.used_themes | set(self.catalog.keys()),
                    excluded_words=self.used_words | self.known_words,
                    timeout=self.api_timeout,
                )
            else:
                generated = fetch_themes_from_openrouter(
                    count=max(self.api_batch_size, minimum_count),
                    min_words=10,
                    max_words=12,
                    excluded_themes=self.used_themes | set(self.catalog.keys()),
                    excluded_words=self.used_words | self.known_words,
                    api_key=self.openrouter_api_key,
                    model=self.openrouter_model,
                    timeout=self.api_timeout,
                )
        except Exception as exc:
            self._dynamic_fetch_disabled = True
            print(
                f"Warning: dynamic theme fetch failed ({exc}). Falling back to the built-in theme catalog.",
                file=sys.stderr,
            )
            return

        for item in generated:
            self._register_theme(item.theme, item.words)

    def available_themes(self) -> List[str]:
        self._ensure_dynamic_themes()
        remaining = [theme for theme in self.catalog if theme not in self.used_themes]
        return sorted(remaining)

    def generate_unique_theme(self) -> str:
        self._ensure_dynamic_themes()
        available = self.available_themes()
        if not available:
            raise ValueError(
                "No unused themes remain. Provide a theme API URL, set OPENROUTER_API_KEY, or expand the local catalog."
            )
        theme = self.rng.choice(available)
        self.used_themes.add(theme)
        return theme

    def get_words_for_theme(self, theme: str, min_words: int = 10, max_words: int = 12) -> List[str]:
        self._ensure_dynamic_themes()
        if theme not in self.catalog:
            raise KeyError(f"Unknown theme: {theme}")

        pool = [word for word in self.catalog[theme] if word not in self.used_words]
        if len(pool) < min_words:
            raise ValueError(
                f"Theme '{theme}' does not have enough unused words for a puzzle."
            )

        target = min(len(pool), self.rng.randint(min_words, max_words))
        selected = self.rng.sample(pool, target)
        self.used_words.update(selected)
        return sorted(selected)

    def theme_count(self) -> int:
        if self._dynamic_fetch_disabled:
            return len(self.catalog)
        return 1_000_000 if (self.api_url or self.openrouter_api_key) else len(self.catalog)
