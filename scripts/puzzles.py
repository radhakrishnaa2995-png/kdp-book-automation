from __future__ import annotations

from dataclasses import dataclass
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
        rows = "|".join("".join(row) for row in self.grid)
        return f"{self.theme}:{rows}:{','.join(self.words)}"
