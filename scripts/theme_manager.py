def _default_catalog() -> Dict[str, List[str]]:
    return {theme: list(words) for theme, words in THEME_CATALOG.items()}


@dataclass
class ThemeManager:
    seed: int | None = None
    api_url: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str | None = None
    api_batch_size: int = 24
    api_timeout: float = 30.0
    catalog: Dict[str, List[str]] = field(default_factory=_default_catalog)

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
