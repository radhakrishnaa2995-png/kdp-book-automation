from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Sequence

from puzzle_generator import Puzzle, generate_grid
from theme_manager import ThemeManager, generate_unique_theme, get_words_for_theme


@dataclass(frozen=True)
class GeneratedBook:
    puzzles: List[Puzzle]
    solutions: List[Puzzle]


def get_grid_size(index: int, total: int, words: Sequence[str]) -> int:
    progress = (index + 1) / max(total, 1)
    preferred = 10 if progress <= 0.33 else 12 if progress <= 0.66 else 15
    longest = max(len(word) for word in words)
    density = sum(len(word) for word in words)

    for size in (10, 12, 15):
        if size < max(preferred, longest):
            continue
        if density / float(size * size) <= 0.72:
            return size
    return 15


def generate_book(puzzle_count: int = 24, seed: int | None = None) -> GeneratedBook:
    manager = ThemeManager(seed=seed)
    if puzzle_count > manager.theme_count():
        raise ValueError(
            f"Requested {puzzle_count} puzzles, but only {manager.theme_count()} unique themes are available."
        )

    rng = random.Random(seed)
    used_signatures: set[str] = set()
    puzzles: List[Puzzle] = []

    for index in range(puzzle_count):
        theme = generate_unique_theme(manager)
        words = get_words_for_theme(theme, manager=manager)
        size = get_grid_size(index, puzzle_count, words)

        puzzle: Puzzle | None = None
        for _ in range(18):
            candidate = generate_grid(
                words=words,
                size=size,
                theme=theme,
                seed=rng.randint(0, 10_000_000),
            )
            if candidate.signature not in used_signatures:
                used_signatures.add(candidate.signature)
                puzzle = candidate
                break

        if puzzle is None:
            raise RuntimeError(f"Unable to generate a non-duplicate puzzle for theme '{theme}'.")

        puzzles.append(puzzle)

    return GeneratedBook(puzzles=puzzles, solutions=list(puzzles))
