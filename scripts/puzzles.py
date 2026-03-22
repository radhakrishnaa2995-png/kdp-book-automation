from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from typing import Dict, Tuple

Coordinate = Tuple[int, int]
Direction = Tuple[int, int]


@dataclass(frozen=True)
class WordPlacement:
    word: str
    start: Coordinate
    end: Coordinate
    direction: Direction
    positions: Tuple[Coordinate, ...]


@dataclass(frozen=True)
class Puzzle:
    theme: str
    grid: Tuple[Tuple[str, ...], ...]
    words: Tuple[str, ...]
    placements: Dict[str, WordPlacement]

    @property
    def signature(self) -> str:
        normalized_grid = "/".join("".join(row) for row in self.grid)
        normalized_words = ",".join(self.words)
        normalized_paths = ";".join(
            f"{word}:{placement.start}->{placement.end}"
            for word, placement in sorted(self.placements.items())
        )
        payload = f"{self.theme}|{normalized_grid}|{normalized_words}|{normalized_paths}"
        return sha1(payload.encode("utf-8")).hexdigest()


def generate_word_search(words, size, theme: str = "Word Search", seed: int | None = None):
    from .grid import generate_puzzle

    grid, placements = generate_puzzle(words, size=size, theme=theme, seed=seed)
    highlight = [position for coords in placements.values() for position in coords]
    return grid, highlight
