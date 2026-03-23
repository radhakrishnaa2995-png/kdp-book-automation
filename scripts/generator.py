from __future__ import annotations

import random
import secrets
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .puzzles import Puzzle
from .puzzle_generator import generate_grid
from .theme_manager import ThemeManager, generate_unique_theme, get_words_for_theme


@dataclass(frozen=True)
class GeneratedBook:
    puzzles: List[Puzzle]
    solutions: List[Puzzle]
    seed: int
    signature: str


GRID_SIZE_OPTIONS: tuple[int, ...] = (10, 12, 15, 18, 20)


def get_grid_sizes(index: int, total: int, words: Sequence[str]) -> List[int]:
    progress = (index + 1) / max(total, 1)
    preferred = 10 if progress <= 0.33 else 12 if progress <= 0.66 else 15
    longest = max(len(word) for word in words)
    density = sum(len(word) for word in words)

    viable_sizes = [size for size in GRID_SIZE_OPTIONS if size >= max(preferred, longest)]
    balanced_sizes = [
        size
        for size in viable_sizes
        if density / float(size * size) <= 0.72
    ]
    if balanced_sizes:
        return balanced_sizes
    return viable_sizes or [max(longest, GRID_SIZE_OPTIONS[-1])]


def get_grid_size(index: int, total: int, words: Sequence[str]) -> int:
    return get_grid_sizes(index, total, words)[0]


def _build_book_signature(puzzles: Iterable[Puzzle]) -> str:
    return "::".join(puzzle.signature for puzzle in puzzles)


def _single_book(
    puzzle_count: int,
    seed: int,
    blocked_page_signatures: set[str] | None = None,
    theme_api_url: str | None = None,
    openrouter_model: str | None = None,
) -> GeneratedBook:
    blocked_page_signatures = blocked_page_signatures or set()
    manager = ThemeManager(seed=seed, api_url=theme_api_url, openrouter_model=openrouter_model)
    if puzzle_count > manager.theme_count():
        raise ValueError(
            f"Requested {puzzle_count} puzzles, but only {manager.theme_count()} unique themes are available."
        )

    rng = random.Random(seed)
    used_signatures: set[str] = set(blocked_page_signatures)
    puzzles: List[Puzzle] = []

    for index in range(puzzle_count):
        theme = generate_unique_theme(manager)
        words = get_words_for_theme(theme, manager=manager)

        puzzle: Puzzle | None = None
        for size in get_grid_sizes(index, puzzle_count, words):
            for _ in range(16):
                try:
                    candidate = generate_grid(
                        words=words,
                        size=size,
                        theme=theme,
                        seed=rng.randint(0, 10_000_000),
                    )
                except RuntimeError:
                    continue
                if candidate.signature not in used_signatures:
                    used_signatures.add(candidate.signature)
                    puzzle = candidate
                    break
            if puzzle is not None:
                break

        if puzzle is None:
            raise RuntimeError(f"Unable to generate a non-duplicate puzzle for theme '{theme}'.")

        puzzles.append(puzzle)

    return GeneratedBook(
        puzzles=puzzles,
        solutions=list(puzzles),
        seed=seed,
        signature=_build_book_signature(puzzles),
    )


def generate_book(
    puzzle_count: int = 24,
    seed: int | None = None,
    blocked_page_signatures: set[str] | None = None,
    blocked_book_signatures: set[str] | None = None,
    max_attempts: int = 24,
    theme_api_url: str | None = None,
    openrouter_model: str | None = None,
) -> GeneratedBook:
    blocked_book_signatures = blocked_book_signatures or set()
    base_seed = seed if seed is not None else secrets.randbits(63)
    seed_rng = random.Random(base_seed)

    for attempt in range(max_attempts):
        book_seed = base_seed if seed is not None and attempt == 0 else seed_rng.randrange(1, 2**63)
        book = _single_book(
            puzzle_count=puzzle_count,
            seed=book_seed,
            blocked_page_signatures=blocked_page_signatures,
            theme_api_url=theme_api_url,
            openrouter_model=openrouter_model,
        )
        if book.signature not in blocked_book_signatures:
            return book

    raise RuntimeError(
        "Unable to generate a unique book after multiple attempts. "
        "Increase the theme catalog or reduce the number of requested PDFs/puzzles."
    )
